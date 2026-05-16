"""
Hardware compatibility checking system.
Analyzes PC builds for issues and provides solutions.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class CompatibilityIssue:
    """Represents a compatibility issue"""
    severity: str  # "error", "warning", "info"
    title: str
    description: str
    components_affected: List[str]
    fix: str
    language: str = "es"

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "severity": self.severity,
            "title": self.title,
            "description": self.description,
            "components_affected": self.components_affected,
            "fix": self.fix,
            "language": self.language
        }


class CompatibilityChecker:
    """Checks hardware compatibility in PC builds"""

    def __init__(self, language: str = "es"):
        self.language = language
        self.socket_compatibility = {
            "Socket 1700": ["Intel Core i9-13900K", "Intel Core i7-13700K"],
            "Socket AM5": ["Ryzen 7 7700X", "Ryzen 9 7950X"],
            "Socket AM4": ["Ryzen 5 5600X", "Ryzen 7 5800X"],
            "LGA1200": ["Intel Core i5-10600K"],
        }

    def check_build(self, build: Dict) -> List[Dict]:
        """
        Check a complete build for compatibility issues.

        Args:
            build: Dictionary with component types and specs

        Returns:
            List of issue dictionaries
        """
        issues = []

        # Extract components
        cpu = build.get("cpu", {})
        motherboard = build.get("motherboard", {})
        ram = build.get("ram", {})
        gpu = build.get("gpu", {})
        psu = build.get("psu", {})
        case = build.get("case", {})
        cooler = build.get("cooler")

        # Run all checks
        issues.extend(self._check_socket_compatibility(cpu, motherboard))
        issues.extend(self._check_ram_compatibility(ram, motherboard))
        issues.extend(self._check_psu_wattage(build))
        issues.extend(self._check_physical_fit(gpu, case))
        issues.extend(self._check_cooler_fit(cooler, case))
        issues.extend(self._check_bottleneck(cpu, gpu))

        return issues

    def _check_socket_compatibility(self, cpu: Dict, motherboard: Dict) -> List[Dict]:
        """Check CPU socket compatibility with motherboard"""
        issues = []

        cpu_socket = cpu.get("socket", "")
        mb_socket = motherboard.get("socket", "")

        if cpu_socket and mb_socket:
            if cpu_socket != mb_socket:
                if self.language == "es":
                    issue = CompatibilityIssue(
                        severity="error",
                        title="Socket Incompatible",
                        description=f"CPU socket {cpu_socket} no coincide con placa madre socket {mb_socket}",
                        components_affected=["CPU", "Motherboard"],
                        fix="Selecciona una CPU o placa madre compatible",
                        language=self.language
                    )
                else:
                    issue = CompatibilityIssue(
                        severity="error",
                        title="Socket Mismatch",
                        description=f"CPU socket {cpu_socket} doesn't match motherboard socket {mb_socket}",
                        components_affected=["CPU", "Motherboard"],
                        fix="Select a compatible CPU or motherboard",
                        language=self.language
                    )
                issues.append(issue.to_dict())

        return issues

    def _check_ram_compatibility(self, ram: Dict, motherboard: Dict) -> List[Dict]:
        """Check RAM type compatibility"""
        issues = []

        ram_type = ram.get("tipo", "")
        mb_ram_type = motherboard.get("ram_tipo", "")

        if ram_type and mb_ram_type:
            if ram_type != mb_ram_type:
                if self.language == "es":
                    issue = CompatibilityIssue(
                        severity="error",
                        title="RAM Incompatible",
                        description=f"RAM tipo {ram_type} no es compatible con placa {mb_ram_type}",
                        components_affected=["RAM", "Motherboard"],
                        fix=f"Usa RAM {mb_ram_type}",
                        language=self.language
                    )
                else:
                    issue = CompatibilityIssue(
                        severity="error",
                        title="Incompatible RAM",
                        description=f"RAM type {ram_type} isn't compatible with motherboard {mb_ram_type}",
                        components_affected=["RAM", "Motherboard"],
                        fix=f"Use {mb_ram_type} RAM",
                        language=self.language
                    )
                issues.append(issue.to_dict())

        # Check RAM slots
        ram_sticks = ram.get("sticks", 1)
        mb_slots = motherboard.get("ram_slots", 4)

        if ram_sticks > mb_slots:
            if self.language == "es":
                issue = CompatibilityIssue(
                    severity="error",
                    title="No hay suficientes slots de RAM",
                    description=f"Necesitas {ram_sticks} sticks pero la placa tiene solo {mb_slots} slots",
                    components_affected=["RAM", "Motherboard"],
                    fix="Reduce la cantidad de sticks de RAM",
                    language=self.language
                )
            else:
                issue = CompatibilityIssue(
                    severity="error",
                    title="Not enough RAM slots",
                    description=f"You need {ram_sticks} sticks but motherboard has only {mb_slots} slots",
                    components_affected=["RAM", "Motherboard"],
                    fix="Reduce the number of RAM sticks",
                    language=self.language
                )
            issues.append(issue.to_dict())

        return issues

    def _check_psu_wattage(self, build: Dict) -> List[Dict]:
        """Check if PSU has adequate wattage"""
        issues = []

        psu_wattage = build.get("psu", {}).get("potencia", 0)
        if psu_wattage == 0:
            return issues

        # Calculate estimated total power draw
        estimated_draw = self._estimate_power_draw(build)
        required_wattage = estimated_draw * 1.2  # 20% headroom

        if psu_wattage < required_wattage:
            if self.language == "es":
                issue = CompatibilityIssue(
                    severity="error",
                    title="Fuente insuficiente",
                    description=f"Tu PC necesita ~{estimated_draw}W, pero seleccionaste {psu_wattage}W",
                    components_affected=["PSU"],
                    fix=f"Usa una fuente de al menos {int(required_wattage)}W",
                    language=self.language
                )
            else:
                issue = CompatibilityIssue(
                    severity="error",
                    title="Insufficient PSU",
                    description=f"Your PC needs ~{estimated_draw}W, but you selected {psu_wattage}W",
                    components_affected=["PSU"],
                    fix=f"Use a PSU of at least {int(required_wattage)}W",
                    language=self.language
                )
            issues.append(issue.to_dict())
        elif psu_wattage < estimated_draw * 1.1:
            if self.language == "es":
                issue = CompatibilityIssue(
                    severity="warning",
                    title="Poco headroom de fuente",
                    description=f"Tu fuente de {psu_wattage}W está muy ajustada para {estimated_draw}W",
                    components_affected=["PSU"],
                    fix="Considera una fuente más potente para mayor estabilidad",
                    language=self.language
                )
            else:
                issue = CompatibilityIssue(
                    severity="warning",
                    title="Low PSU headroom",
                    description=f"Your {psu_wattage}W PSU is tight for {estimated_draw}W",
                    components_affected=["PSU"],
                    fix="Consider a more powerful PSU for stability",
                    language=self.language
                )
            issues.append(issue.to_dict())

        return issues

    def _check_physical_fit(self, gpu: Dict, case: Dict) -> List[Dict]:
        """Check if GPU fits in case"""
        issues = []

        gpu_length = gpu.get("largo_mm", 0)
        case_max_gpu = case.get("max_gpu_mm", 0)

        if gpu_length > 0 and case_max_gpu > 0:
            if gpu_length > case_max_gpu:
                if self.language == "es":
                    issue = CompatibilityIssue(
                        severity="error",
                        title="GPU no cabe en el gabinete",
                        description=f"GPU de {gpu_length}mm no cabe en gabinete de {case_max_gpu}mm",
                        components_affected=["GPU", "Case"],
                        fix="Elige un gabinete más grande o una GPU más pequeña",
                        language=self.language
                    )
                else:
                    issue = CompatibilityIssue(
                        severity="error",
                        title="GPU doesn't fit in case",
                        description=f"GPU of {gpu_length}mm doesn't fit in case with {case_max_gpu}mm max",
                        components_affected=["GPU", "Case"],
                        fix="Choose a larger case or smaller GPU",
                        language=self.language
                    )
                issues.append(issue.to_dict())

        return issues

    def _check_cooler_fit(self, cooler: Optional[Dict], case: Dict) -> List[Dict]:
        """Check if cooler fits in case"""
        issues = []

        if not cooler:
            return issues

        cooler_height = cooler.get("altura_mm", 0)
        case_max_cooler = case.get("max_cooler_mm", 0)

        if cooler_height > 0 and case_max_cooler > 0:
            if cooler_height > case_max_cooler:
                if self.language == "es":
                    issue = CompatibilityIssue(
                        severity="error",
                        title="Cooler no cabe en el gabinete",
                        description=f"Cooler de {cooler_height}mm no cabe en gabinete de {case_max_cooler}mm",
                        components_affected=["Cooler", "Case"],
                        fix="Elige un cooler más pequeño o un gabinete más grande",
                        language=self.language
                    )
                else:
                    issue = CompatibilityIssue(
                        severity="error",
                        title="Cooler doesn't fit in case",
                        description=f"Cooler of {cooler_height}mm doesn't fit in case with {case_max_cooler}mm max",
                        components_affected=["Cooler", "Case"],
                        fix="Choose a smaller cooler or larger case",
                        language=self.language
                    )
                issues.append(issue.to_dict())

        return issues

    def _check_bottleneck(self, cpu: Dict, gpu: Dict) -> List[Dict]:
        """Detect CPU/GPU bottleneck"""
        issues = []

        cpu_name = cpu.get("nombre", "").lower()
        gpu_name = gpu.get("nombre", "").lower()

        cpu_tier = self._get_cpu_tier(cpu_name)
        gpu_tier = self._get_gpu_tier(gpu_name)

        # Simple bottleneck heuristic
        if cpu_tier > 0 and gpu_tier > 0:
            diff = abs(cpu_tier - gpu_tier)
            if diff >= 3:
                if self.language == "es":
                    issue = CompatibilityIssue(
                        severity="warning",
                        title="Posible cuello de botella",
                        description=f"Hay un desbalance entre CPU (tier {cpu_tier}) y GPU (tier {gpu_tier})",
                        components_affected=["CPU", "GPU"],
                        fix="Equilibra la calidad de CPU y GPU para mejor rendimiento",
                        language=self.language
                    )
                else:
                    issue = CompatibilityIssue(
                        severity="warning",
                        title="Possible bottleneck",
                        description=f"Imbalance between CPU (tier {cpu_tier}) and GPU (tier {gpu_tier})",
                        components_affected=["CPU", "GPU"],
                        fix="Balance CPU and GPU quality for better performance",
                        language=self.language
                    )
                issues.append(issue.to_dict())

        return issues

    def _estimate_power_draw(self, build: Dict) -> int:
        """Estimate total power draw from components"""
        draw = 0

        # CPU TDP
        cpu_tdp = build.get("cpu", {}).get("tdp", 0)
        if cpu_tdp > 0:
            draw += cpu_tdp

        # GPU TDP
        gpu_tdp = build.get("gpu", {}).get("tdp", 0)
        if gpu_tdp > 0:
            draw += gpu_tdp

        # Rest of system (motherboard, RAM, storage, fans, etc.)
        draw += 150

        return draw

    def _get_cpu_tier(self, cpu_name: str) -> int:
        """Get CPU performance tier (0-10)"""
        if "i9" in cpu_name:
            return 9
        elif "i7" in cpu_name or "ryzen 9" in cpu_name:
            return 8
        elif "i5" in cpu_name or "ryzen 7" in cpu_name:
            return 6
        elif "i3" in cpu_name or "ryzen 5" in cpu_name:
            return 4
        elif "ryzen 3" in cpu_name:
            return 3
        return 0

    def _get_gpu_tier(self, gpu_name: str) -> int:
        """Get GPU performance tier (0-10)"""
        if "4090" in gpu_name or "rtx 4090" in gpu_name:
            return 10
        elif "4080" in gpu_name or "4070" in gpu_name:
            return 8
        elif "4060" in gpu_name or "3080" in gpu_name:
            return 6
        elif "1660" in gpu_name or "3060" in gpu_name:
            return 4
        elif "1650" in gpu_name:
            return 2
        return 0
