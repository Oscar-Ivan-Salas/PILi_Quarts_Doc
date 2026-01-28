# 🎨 PALETA DE COLORES - TESLA COTIZADOR V3.0

## 🔴 COLORES PRINCIPALES

### Rojo Tesla (Principal)
```css
--color-tesla-red: #8B0000
```
**Uso:** Fondo de header, botones principales, acentos

### Dorado Tesla (Secundario)
```css
--color-tesla-gold: #D4AF37
```
**Uso:** Texto destacado, bordes, botones secundarios

### Negro
```css
--color-black: #000000
```
**Uso:** Fondo base, texto

### Gris Oscuro
```css
--color-gray-dark: #1f2937
```
**Uso:** Cards, contenedores, efectos glass

---

## 🌈 ESCALA COMPLETA DE ROJOS (Tailwind)

```javascript
tesla-red-50:  #fef2f2  // Muy claro
tesla-red-100: #fee2e2
tesla-red-200: #fecaca
tesla-red-300: #fca5a5
tesla-red-400: #f87171
tesla-red-500: #ef4444
tesla-red-600: #dc2626
tesla-red-700: #b91c1c
tesla-red-800: #991b1b
tesla-red-900: #8B0000  // ⭐ PRINCIPAL
tesla-red-950: #450a0a  // Muy oscuro
```

---

## 🌟 ESCALA COMPLETA DE DORADOS (Tailwind)

```javascript
tesla-gold-50:  #fefce8  // Muy claro
tesla-gold-100: #fef9c3
tesla-gold-200: #fef08a
tesla-gold-300: #fde047
tesla-gold-400: #facc15
tesla-gold-500: #D4AF37  // ⭐ PRINCIPAL
tesla-gold-600: #ca8a04
tesla-gold-700: #a16207
tesla-gold-800: #854d0e
tesla-gold-900: #713f12  // Muy oscuro
```

---

## 🎭 DEGRADADOS

### Fondo del Body
```css
background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
```
**De:** Negro puro → **A:** Gris muy oscuro

### Scrollbar Thumb
```css
background: linear-gradient(180deg, #D4AF37 0%, #b8941f 100%);
```
**De:** Dorado claro → **A:** Dorado oscuro

### Texto Degradado
```css
background: linear-gradient(135deg, #D4AF37 0%, #FFD700 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
```
**De:** Dorado Tesla → **A:** Dorado brillante

### Botón Primary
```css
background: linear-gradient(to right, tesla-red-900, tesla-red-800);
```
**De:** #8B0000 → **A:** #991b1b

### Botón Secondary
```css
background: linear-gradient(to right, tesla-gold-500, tesla-gold-600);
```
**De:** #D4AF37 → **A:** #ca8a04

---

## 💧 TRANSPARENCIAS (RGBA)

### Glass Effect
```css
background: rgba(31, 41, 55, 0.8);
backdrop-filter: blur(10px);
border: 1px solid rgba(255, 255, 255, 0.1);
```
**Color:** Gris oscuro con 80% opacidad
**Efecto:** Vidrio esmerilado

### Sombra Glow (Dorado)
```css
box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
/* Hover: */
box-shadow: 0 0 40px rgba(212, 175, 55, 0.8);
```

---

## 🌑 SOMBRAS

### Sombra Tesla (Roja)
```css
box-shadow: 0 10px 40px rgba(139, 0, 0, 0.3);
```

### Sombra Gold (Dorada)
```css
box-shadow: 0 10px 40px rgba(212, 175, 55, 0.3);
```

### Sombra Hover Lift
```css
box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
```

---

## 📋 PARA PILI ITSE - COLORES RECOMENDADOS

### Basado en el archivo original `pili-itse-complete-review.txt`:

#### Fondo Principal
```javascript
background: linear-gradient(135deg, #2C0000 0%, #8B0000 50%, #FF4500 100%)
```
**De:** Rojo muy oscuro → **A través de:** Rojo Tesla → **A:** Naranja fuego

#### Header
```javascript
background: linear-gradient(90deg, #8B0000, #FF4500)
borderBottom: 3px solid #D4AF37
```

#### Logo Circle
```javascript
background: linear-gradient(135deg, #D4AF37, #FFA500)
boxShadow: 0 0 20px rgba(255, 215, 0, 0.5)
border: 3px solid #8B0000
```

#### Burbujas de PILI (Bot)
```javascript
background: linear-gradient(135deg, #8B0000, #FF4500)
color: white
```

#### Burbujas de Usuario
```javascript
background: linear-gradient(135deg, #D4AF37, #FFA500)
color: #2C0000  // Texto oscuro
```

#### Botones
```javascript
background: white
color: #8B0000
border: 2px solid #D4AF37
/* Hover: */
background: #D4AF37
transform: scale(1.05)
```

#### Input Field
```javascript
background: white
border: 2px solid #D4AF37
borderRadius: 25px
```

#### Footer
```javascript
background: rgba(0, 0, 0, 0.3)
color: white
```

---

## 🎯 RESUMEN PARA IMPLEMENTACIÓN

### Colores que DEBES usar para PILI ITSE:

1. **Fondo degradado:** `#2C0000` → `#8B0000` → `#FF4500`
2. **Burbujas PILI:** `#8B0000` → `#FF4500` (degradado rojo-naranja)
3. **Burbujas Usuario:** `#D4AF37` → `#FFA500` (degradado dorado-naranja)
4. **Botones:** Fondo blanco, borde `#D4AF37`, hover dorado
5. **Header:** `#8B0000` → `#FF4500` con borde dorado
6. **Logo:** Círculo dorado con rayo amarillo
7. **Footer:** Negro transparente `rgba(0,0,0,0.3)`

---

## 📝 CÓDIGOS HEXADECIMALES CLAVE

```
#2C0000 - Rojo muy oscuro (fondo base)
#8B0000 - Rojo Tesla (principal)
#FF4500 - Naranja fuego (acento)
#D4AF37 - Dorado Tesla (secundario)
#FFA500 - Naranja dorado (acento cálido)
#FFD700 - Dorado brillante (highlights)
#000000 - Negro puro
#1a1a1a - Gris muy oscuro
#1f2937 - Gris oscuro (glass effect)
```
