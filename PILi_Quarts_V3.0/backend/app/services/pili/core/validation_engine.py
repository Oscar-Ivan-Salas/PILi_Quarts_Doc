"""
✅ VALIDATION ENGINE - Motor de Validación Reutilizable
Maneja toda la lógica de validación de datos
"""

import re
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class ValidationEngine:
    """Motor de validación reutilizable para todos los especialistas"""
    
    def validate_number(
        self,
        value: str,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None,
        value_type: str = "float"
    ) -> Tuple[bool, Optional[float], str]:
        """
        Valida un número
        
        Args:
            value: Valor a validar
            min_val: Valor mínimo permitido
            max_val: Valor máximo permitido
            value_type: Tipo de número ("int" o "float")
        
        Returns:
            (es_valido, numero, mensaje_error)
        """
        # Limpiar valor
        value = str(value).strip().replace(",", ".")
        
        # Intentar convertir
        try:
            if value_type == "int":
                numero = int(float(value))
            else:
                numero = float(value)
        except ValueError:
            return (False, None, "❌ Por favor ingresa un número válido")
        
        # Validar rango mínimo
        if min_val is not None and numero < min_val:
            return (False, None, f"❌ El valor debe ser mayor o igual a {min_val}")
        
        # Validar rango máximo
        if max_val is not None and numero > max_val:
            return (False, None, f"❌ El valor debe ser menor o igual a {max_val}")
        
        return (True, numero, "")
    
    def validate_email(self, email: str) -> Tuple[bool, str]:
        """
        Valida un email
        
        Args:
            email: Email a validar
        
        Returns:
            (es_valido, mensaje_error)
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(pattern, email.strip()):
            return (True, "")
        
        return (False, "❌ Email inválido. Formato esperado: ejemplo@correo.com")
    
    def validate_phone(self, phone: str) -> Tuple[bool, str]:
        """
        Valida un teléfono
        
        Args:
            phone: Teléfono a validar
        
        Returns:
            (es_valido, mensaje_error)
        """
        # Limpiar (quitar espacios, guiones, paréntesis)
        phone_clean = re.sub(r'[^\d]', '', phone)
        
        # Validar longitud (mínimo 9 dígitos para Perú)
        if len(phone_clean) >= 9:
            return (True, "")
        
        return (False, "❌ Teléfono debe tener al menos 9 dígitos")
    
    def validate_ruc(self, ruc: str) -> Tuple[bool, str]:
        """
        Valida un RUC peruano
        
        Args:
            ruc: RUC a validar
        
        Returns:
            (es_valido, mensaje_error)
        """
        # Limpiar
        ruc_clean = re.sub(r'[^\d]', '', ruc)
        
        # RUC debe tener 11 dígitos
        if len(ruc_clean) != 11:
            return (False, "❌ RUC debe tener 11 dígitos")
        
        # Validar que empiece con 10 o 20
        if not (ruc_clean.startswith('10') or ruc_clean.startswith('20')):
            return (False, "❌ RUC debe empezar con 10 o 20")
        
        return (True, "")
    
    def validate_text(
        self,
        text: str,
        min_length: int = 1,
        max_length: int = 500
    ) -> Tuple[bool, str]:
        """
        Valida un texto
        
        Args:
            text: Texto a validar
            min_length: Longitud mínima
            max_length: Longitud máxima
        
        Returns:
            (es_valido, mensaje_error)
        """
        text = text.strip()
        
        if len(text) < min_length:
            return (False, f"❌ El texto debe tener al menos {min_length} caracteres")
        
        if len(text) > max_length:
            return (False, f"❌ El texto no puede exceder {max_length} caracteres")
        
        return (True, "")
    
    def validate_selection(
        self,
        value: str,
        valid_options: list
    ) -> Tuple[bool, str]:
        """
        Valida que un valor esté en una lista de opciones válidas
        
        Args:
            value: Valor a validar
            valid_options: Lista de opciones válidas
        
        Returns:
            (es_valido, mensaje_error)
        """
        if value in valid_options:
            return (True, "")
        
        return (False, f"❌ Opción inválida. Opciones válidas: {', '.join(valid_options)}")
