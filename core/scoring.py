"""
Build scoring system - rates PC builds based on multiple factors.
"""

from typing import Dict, List


class BuildScorer:
    """Scores PC builds for quality and value"""

    def __init__(self, language: str = "es"):
        self.language = language

    def score_build(self, build: Dict) -> Dict:
        """
        Score a complete build (1-10 scale).

        Returns: {"overall": 7.5, "breakdown": {}}
        """
        scores = {
            "performance": self._score_performance(build),
            "value": self._score_value(build),
            "compatibility": self._score_compatibility(build),
            "balance": self._score_balance(build),
        }

        # Weighted average
        overall = (
            scores["performance"] * 0.35 +
            scores["value"] * 0.25 +
            scores["compatibility"] * 0.25 +
            scores["balance"] * 0.15
        )

        return {
            "overall": round(overall, 1),
            "breakdown": scores,
            "rating": self._get_rating_text(overall)
        }

    def _score_performance(self, build: Dict) -> float:
        """Score CPU/GPU performance"""
        cpu_name = build.get("cpu", {}).get("nombre", "").lower()
        gpu_name = build.get("gpu", {}).get("nombre", "").lower()

        cpu_score = self._rate_cpu(cpu_name)
        gpu_score = self._rate_gpu(gpu_name)

        return (cpu_score + gpu_score) / 2

    def _score_value(self, build: Dict) -> float:
        """Score price-to-performance"""
        # Simulated scoring based on component tiers
        cpu_price = build.get("cpu", {}).get("precio", 300)
        gpu_price = build.get("gpu", {}).get("precio", 500)
        ram_price = build.get("ram", {}).get("precio", 120)

        total_price = cpu_price + gpu_price + ram_price

        if total_price < 500:
            return 9
        elif total_price < 1000:
            return 8
        elif total_price < 2000:
            return 7
        else:
            return 6

    def _score_compatibility(self, build: Dict) -> float:
        """Score compatibility (fewer issues = higher score)"""
        # In real app, use CompatibilityChecker here
        return 8.5

    def _score_balance(self, build: Dict) -> float:
        """Score CPU/GPU balance"""
        cpu_tier = self._get_cpu_tier(build.get("cpu", {}).get("nombre", "").lower())
        gpu_tier = self._get_gpu_tier(build.get("gpu", {}).get("nombre", "").lower())

        diff = abs(cpu_tier - gpu_tier)
        if diff <= 1:
            return 10
        elif diff <= 2:
            return 8
        else:
            return 6

    def value_score(self, component: Dict) -> float:
        """Score component value (1-10)"""
        price = component.get("precio", 0)
        if price == 0:
            return 5
        elif price < 100:
            return 9
        elif price < 300:
            return 8
        elif price < 600:
            return 7
        elif price < 1000:
            return 6
        else:
            return 5

    def _rate_cpu(self, cpu_name: str) -> float:
        """Rate CPU performance"""
        if "i9" in cpu_name:
            return 9.5
        elif "i7" in cpu_name or "ryzen 9" in cpu_name:
            return 8.5
        elif "i5" in cpu_name or "ryzen 7" in cpu_name:
            return 7
        elif "i3" in cpu_name or "ryzen 5" in cpu_name:
            return 5
        return 4

    def _rate_gpu(self, gpu_name: str) -> float:
        """Rate GPU performance"""
        if "4090" in gpu_name:
            return 9.5
        elif "4080" in gpu_name or "4070" in gpu_name:
            return 8.5
        elif "3080" in gpu_name or "4060" in gpu_name:
            return 7
        elif "3070" in gpu_name or "1660" in gpu_name:
            return 6
        elif "1650" in gpu_name:
            return 4
        return 3

    def _get_cpu_tier(self, cpu_name: str) -> int:
        """Get CPU tier"""
        if "i9" in cpu_name:
            return 9
        elif "i7" in cpu_name or "ryzen 9" in cpu_name:
            return 8
        elif "i5" in cpu_name or "ryzen 7" in cpu_name:
            return 6
        elif "i3" in cpu_name or "ryzen 5" in cpu_name:
            return 4
        return 0

    def _get_gpu_tier(self, gpu_name: str) -> int:
        """Get GPU tier"""
        if "4090" in gpu_name:
            return 10
        elif "4080" in gpu_name or "4070" in gpu_name:
            return 8
        elif "3080" in gpu_name or "4060" in gpu_name:
            return 6
        elif "1660" in gpu_name or "3070" in gpu_name:
            return 4
        return 0

    def _get_rating_text(self, score: float) -> str:
        """Get text rating based on score"""
        if self.language == "es":
            if score >= 9:
                return "🏆 Excelente"
            elif score >= 8:
                return "👍 Muy Bueno"
            elif score >= 7:
                return "✅ Bueno"
            elif score >= 6:
                return "⚠️ Aceptable"
            else:
                return "❌ Pobre"
        else:
            if score >= 9:
                return "🏆 Excellent"
            elif score >= 8:
                return "👍 Very Good"
            elif score >= 7:
                return "✅ Good"
            elif score >= 6:
                return "⚠️ Fair"
            else:
                return "❌ Poor"
