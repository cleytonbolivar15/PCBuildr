"""
PCBuildr Build Analysis Module
Analyzes PC builds for compatibility, performance, and recommendations
"""

class BuildAnalyzer:
    """Analyzes PC builds for compatibility and recommendations"""
    
    def __init__(self):
        self.cpu_scores = {
            "i3": 30, "i5": 60, "i7": 85, "i9": 95,
            "ryzen 3": 32, "ryzen 5": 65, "ryzen 7": 88, "ryzen 9": 95
        }
        self.gpu_scores = {
            "1660": 50, "3060": 70, "3080": 90, "4090": 100,
            "6600": 48, "6800": 88, "6900": 98
        }
    
    def analyze_build(self, components: dict) -> dict:
        """Analyze a complete build and return metrics"""
        analysis = {
            "compatibility_issues": [],
            "performance_score": 0,
            "power_estimate": 0,
            "bottleneck_analysis": "",
            "recommendations": [],
            "build_tier": "Not configured"
        }
        
        # Check for component presence
        cpu = components.get("cpu")
        gpu = components.get("gpu")
        ram = components.get("ram")
        psu = components.get("psu")
        storage = components.get("storage")
        
        # Validate basic build
        if not cpu:
            analysis["compatibility_issues"].append("No CPU selected")
        if not ram:
            analysis["compatibility_issues"].append("No RAM selected")
        if not psu:
            analysis["compatibility_issues"].append("No PSU selected")
        if not storage:
            analysis["compatibility_issues"].append("No Storage selected")
        
        # Calculate performance
        if cpu or gpu:
            cpu_score = self._get_cpu_score(cpu) if cpu else 0
            gpu_score = self._get_gpu_score(gpu) if gpu else 0
            analysis["performance_score"] = (cpu_score + gpu_score) / 2
            analysis["build_tier"] = self._get_tier(analysis["performance_score"])
        
        # Estimate power
        if cpu or gpu:
            base_power = 250  # Base system power
            cpu_power = 65 if "ryzen 5" in (cpu or "").lower() or "i5" in (cpu or "").lower() else 125
            gpu_power = 250 if gpu and ("4060" in gpu or "3060" in gpu) else 350
            analysis["power_estimate"] = base_power + cpu_power + gpu_power
        
        # Check for bottlenecks
        if cpu and gpu:
            analysis["bottleneck_analysis"] = self._check_bottleneck(cpu, gpu)
        
        # Add recommendations
        analysis["recommendations"] = self._get_recommendations(components, analysis)
        
        return analysis
    
    def _get_cpu_score(self, cpu_name: str) -> int:
        """Get performance score for CPU"""
        cpu_lower = cpu_name.lower()
        for key, score in self.cpu_scores.items():
            if key in cpu_lower:
                return score
        return 40  # Default
    
    def _get_gpu_score(self, gpu_name: str) -> int:
        """Get performance score for GPU"""
        gpu_lower = gpu_name.lower()
        for key, score in self.gpu_scores.items():
            if key in gpu_lower:
                return score
        return 35  # Default
    
    def _get_tier(self, score: float) -> str:
        """Get build tier based on score"""
        if score < 30:
            return "Entry-Level"
        elif score < 60:
            return "Mid-Range"
        elif score < 85:
            return "High-End"
        else:
            return "Enthusiast"
    
    def _check_bottleneck(self, cpu: str, gpu: str) -> str:
        """Check for CPU/GPU bottleneck"""
        cpu_score = self._get_cpu_score(cpu)
        gpu_score = self._get_gpu_score(gpu)
        
        diff = abs(cpu_score - gpu_score)
        if diff > 30:
            if cpu_score < gpu_score:
                return "Potential CPU bottleneck - GPU might be underutilized"
            else:
                return "Potential GPU bottleneck - CPU underutilized"
        return "Balanced CPU/GPU pairing"
    
    def _get_recommendations(self, components: dict, analysis: dict) -> list:
        """Get recommendations for the build"""
        recs = []
        
        if not components.get("cpu"):
            recs.append("Select a CPU to get started")
        
        if analysis["power_estimate"] > 0 and analysis["power_estimate"] > 600:
            psu_str = components.get("psu", "0")
            # Extract wattage from PSU string (e.g., "Corsair CV550 550W 80+ Bronze" -> 550)
            psu_watts = 0
            for word in psu_str.split():
                if word.endswith("W") and word[:-1].isdigit():
                    psu_watts = int(word[:-1])
                    break
            if psu_watts > 0 and psu_watts < analysis["power_estimate"]:
                recs.append(f"Consider a higher wattage PSU ({analysis['power_estimate']}W+ recommended)")
        
        if analysis["performance_score"] < 50 and components.get("gpu"):
            recs.append("Consider upgrading GPU for better gaming performance")
        
        if not components.get("storage") or len(components.get("storage", "")) < 5:
            recs.append("Add SSD storage for better boot/load times")
        
        if not recs:
            recs.append("Build looks good! Consider your use case and budget.")
        
        return recs
