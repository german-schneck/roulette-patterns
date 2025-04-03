# Simulador de Estrategias de Ruleta

## Concepto del Proyecto

Este proyecto es un simulador de estrategias para el juego de ruleta que permite evaluar y comparar diferentes métodos de apuestas en un entorno controlado. El simulador implementa varias estrategias clásicas y originales, permitiendo analizar su comportamiento, rentabilidad y riesgo a largo plazo.

## Objetivo

El objetivo principal de este simulador es proporcionar una herramienta para:

- Analizar el rendimiento de diferentes estrategias de apuestas en la ruleta
- Comparar resultados entre distintos métodos bajo las mismas condiciones
- Visualizar la evolución del bankroll a lo largo de múltiples sesiones de juego
- Identificar las fortalezas y debilidades de cada estrategia
- Servir como plataforma educativa sobre probabilidad y gestión de riesgo en juegos de azar

Este proyecto tiene fines educativos y de investigación, y busca demostrar matemáticamente por qué ninguna estrategia puede superar la ventaja de la casa a largo plazo, a pesar de que algunas puedan ofrecer mejores resultados a corto plazo o una gestión más eficiente del riesgo.

## Instrucciones de Uso

Para ejecutar el simulador, utiliza el siguiente comando:

```bash
python main.py --initial-bankroll 1000 --num-simulations 100 --min-bet 1 --max-spins 1000 --profit-target 50
```

Parámetros disponibles:
- `--initial-bankroll`: Bankroll inicial para cada simulación (por defecto: 1000.0)
- `--num-simulations`: Número de simulaciones a ejecutar por estrategia (por defecto: 100)
- `--min-bet`: Apuesta mínima permitida (por defecto: 1.0)
- `--max-spins`: Número máximo de tiradas por sesión (por defecto: 1000)
- `--profit-target`: Objetivo de ganancia como porcentaje del bankroll inicial (por defecto: 50.0)
- `--output-plot`: Ruta del archivo de gráfico de resultados (por defecto: 'results.png')

## Estrategias Implementadas

El simulador incluye 26 estrategias diferentes agrupadas en categorías. A continuación se presenta una descripción detallada de cada una, distinguiendo entre estrategias reales (documentadas en la literatura de juegos de azar) y estrategias inventadas (creadas específicamente para este simulador).

### Estrategias Clásicas

#### Estrategias Reales

1. **MartingaleStrategy (Martingala)**
   - **Descripción**: Sistema de progresión negativa donde se duplica la apuesta después de cada pérdida.
   - **Funcionamiento**: Apuesta en opciones simples (rojo/negro, par/impar) y duplica la apuesta tras perder.
   - **Ventajas**: Potencialmente efectiva en rachas cortas de pérdida.
   - **Desventajas**: Riesgo exponencial y posibilidad de alcanzar el límite de apuesta.

2. **FibonacciStrategy (Fibonacci)**
   - **Descripción**: Utiliza la secuencia de Fibonacci para determinar el tamaño de las apuestas.
   - **Funcionamiento**: Incrementa la apuesta según la secuencia tras perder y retrocede dos números tras ganar.
   - **Ventajas**: Progresión menos agresiva que la Martingala.
   - **Desventajas**: Puede llevar a apuestas grandes tras varias pérdidas consecutivas.

3. **ParoliStrategy (Paroli)**
   - **Descripción**: Sistema de progresión positiva que aumenta la apuesta después de victorias.
   - **Funcionamiento**: Apuesta en opciones simples y duplica la apuesta tras cada victoria, hasta completar 3 victorias consecutivas.
   - **Ventajas**: Limita pérdidas y capitaliza rachas ganadoras.
   - **Desventajas**: Requiere victorias consecutivas para ser efectiva.

4. **DAlembertStrategy (D'Alembert)**
   - **Descripción**: Basada en el equilibrio matemático propuesto por el físico D'Alembert.
   - **Funcionamiento**: Incrementa la apuesta en una unidad tras perder y disminuye en una unidad tras ganar.
   - **Ventajas**: Progresión moderada con menor riesgo que Martingala.
   - **Desventajas**: Recuperación lenta de pérdidas.

#### Estrategias Inventadas

5. **PatternStrategy**
   - **Descripción**: Sistema ficticio que busca patrones en los números ganadores anteriores.
   - **Funcionamiento**: Registra secuencias de números y apuesta basándose en patrones detectados.
   - **Ventajas**: Adaptable a condiciones cambiantes.
   - **Desventajas**: Basada en la falacia del jugador, sin base matemática sólida.

6. **OscarStrategy**
   - **Descripción**: Estrategia inventada de gestión de bankroll y unidades de apuesta.
   - **Funcionamiento**: Define una unidad objetivo de ganancia y ajusta las apuestas para alcanzarla.
   - **Ventajas**: Enfoque disciplinado con objetivos claros.
   - **Desventajas**: Puede llevar a largos periodos sin alcanzar el objetivo.

### Estrategias Asiáticas (Todas Inventadas)

7. **DragonTigerStrategy (Dragón y Tigre)**
   - **Descripción**: Inspirada en el juego asiático de Dragón y Tigre.
   - **Funcionamiento**: Alterna entre números "dragón" (altos) y "tigre" (bajos) según un patrón de ritmo.
   - **Ventajas**: Cobertura de diferentes sectores de la ruleta.
   - **Desventajas**: Complejidad en su seguimiento y ejecución.

8. **GoldenEagleStrategy (Águila Dorada)**
   - **Descripción**: Basada en conceptos de numerología asiática y números "dorados".
   - **Funcionamiento**: Identifica números "dorados" (2, 5, 8, etc.) y aplica una progresión específica.
   - **Ventajas**: Enfoque en un conjunto específico de números con altas apuestas.
   - **Desventajas**: Cobertura limitada de la mesa.

9. **Lucky8Strategy (Suerte 8)**
   - **Descripción**: Centrada en el número 8 y sus derivados, considerados de buena suerte en culturas asiáticas.
   - **Funcionamiento**: Apuesta en el 8 y números relacionados con progresión variable.
   - **Ventajas**: Concentración de recursos en números específicos.
   - **Desventajas**: Alta varianza debido a la concentración de apuestas.

### Estrategias de Las Vegas (Reales)

10. **LabouchereStrategy (Labouchere)**
    - **Descripción**: También conocida como "cancelación" o "tachado", popular en casinos occidentales.
    - **Funcionamiento**: Utiliza una secuencia de números para determinar el monto de apuesta. Se tacha los números de los extremos cuando se gana.
    - **Ventajas**: Sistema estructurado con meta definida de ganancia.
    - **Desventajas**: Puede llevar a apuestas muy altas tras varias pérdidas.

11. **OneThreeTwoSixStrategy (1-3-2-6)**
    - **Descripción**: Sistema de progresión para maximizar ganancias en rachas favorables.
    - **Funcionamiento**: Sigue un patrón de apuestas de 1, 3, 2 y 6 unidades sobre victorias consecutivas.
    - **Ventajas**: Limita pérdidas y asegura ganancias en rachas favorables.
    - **Desventajas**: Requiere 4 victorias consecutivas para maximizar beneficio.

12. **JamesBondStrategy (Estrategia James Bond)**
    - **Descripción**: Sistema de cobertura fijo popularizado por las novelas de Ian Fleming y su personaje James Bond.
    - **Funcionamiento**: Distribución fija de apuestas que cubre 25 de los 37 números de la ruleta europea.
    - **Ventajas**: Alta probabilidad de ganar en cada tirada (cubre aproximadamente el 67% de la mesa).
    - **Desventajas**: Requiere unidades de apuesta relativamente altas (20 unidades por tirada) y pagos variables.

### Estrategias Latinoamericanas (Todas Inventadas)

13. **TulumStrategy (México)**
    - **Descripción**: Inspirada en la cultura maya y las ruinas de Tulum.
    - **Funcionamiento**: Utiliza ciclos basados en el calendario maya para ajustar apuestas y números.
    - **Ventajas**: Incorpora adaptabilidad cíclica a diferentes condiciones de juego.
    - **Desventajas**: Complejidad en su implementación.

14. **AndinaStrategy (Región Andina)**
    - **Descripción**: Basada en la cosmovisión andina y el concepto de reciprocidad.
    - **Funcionamiento**: Alterna entre números altos y bajos según un balance inspirado en la dualidad andina.
    - **Ventajas**: Busca equilibrio entre riesgo y recompensa.
    - **Desventajas**: Puede ser demasiado conservadora en algunas situaciones.

15. **CaracasStrategy (Venezuela)**
    - **Descripción**: Inspirada en el ritmo caraqueño y las corrientes de petróleo.
    - **Funcionamiento**: Incrementa y disminuye apuestas en ciclos, como las fluctuaciones petroleras.
    - **Ventajas**: Adaptable a diferentes condiciones de mercado.
    - **Desventajas**: Alta volatilidad en resultados.

16. **TangoStrategy (Argentina)**
    - **Descripción**: Basada en los pasos del tango argentino y sus figuras icónicas.
    - **Funcionamiento**: Utiliza una progresión de apuestas inspirada en los movimientos del tango.
    - **Ventajas**: Equilibrio entre agresividad y conservadurismo.
    - **Desventajas**: Requiere seguimiento preciso de la secuencia.

17. **CariocaStrategy (Brasil)**
    - **Descripción**: Inspirada en el carnaval de Río y las escuelas de samba.
    - **Funcionamiento**: Categoriza números por "escuelas de samba" y alterna entre ellas con progresión rítmica.
    - **Ventajas**: Cobertura amplia de diferentes sectores de la ruleta.
    - **Desventajas**: Sistema complejo que requiere seguimiento detallado.

18. **ValparaisoStrategy (Chile)**
    - **Descripción**: Inspirada en los coloridos cerros de Valparaíso.
    - **Funcionamiento**: Divide la ruleta en sectores de "cerros" y alterna entre ellos según resultados.
    - **Ventajas**: Adaptabilidad a tendencias en sectores específicos.
    - **Desventajas**: Puede llevar a concentración excesiva en sectores no ganadores.

19. **MontevideoStrategy (Uruguay)**
    - **Descripción**: Basada en barrios de Montevideo y la influencia del Río de la Plata.
    - **Funcionamiento**: Sistema de "barrios" con diferentes conjuntos de números y un mecanismo de "nivel del río" para ajustar apuestas.
    - **Ventajas**: Flexibilidad para adaptarse a diferentes condiciones.
    - **Desventajas**: Múltiples variables que controlar durante el juego.

### Estrategias Vetadas de Casinos (Inspiradas en métodos reales pero implementaciones ficticias)

20. **KesselguckenStrategy**
    - **Descripción**: Inspirada en la técnica alemana de "mirar el kessel" (cilindro) para predecir sectores.
    - **Funcionamiento**: Analiza patrones físicos y sectores de caída en la rueda.
    - **Ventajas**: Enfoque en la física real del juego en lugar de probabilidades abstractas.
    - **Desventajas**: En la vida real requiere observación intensa; en el simulador es una aproximación.

21. **GrandeMartingaleStrategy**
    - **Descripción**: Versión más agresiva de la Martingala clásica.
    - **Funcionamiento**: Duplica la apuesta tras pérdidas y añade unidades adicionales para acelerar la recuperación.
    - **Ventajas**: Recuperación más rápida tras una victoria.
    - **Desventajas**: Incremento exponencial del riesgo con cada pérdida.

22. **ThorpSystemStrategy**
    - **Descripción**: Inspirada en las técnicas del matemático Edward Thorp, pionero en el conteo de cartas.
    - **Funcionamiento**: Utiliza análisis estadístico y el criterio de Kelly para optimizar apuestas.
    - **Ventajas**: Enfoque matemáticamente sofisticado para la gestión de bankroll.
    - **Desventajas**: Complejidad de implementación y seguimiento.

23. **MonacoSystemStrategy**
    - **Descripción**: Basada en técnicas supuestamente utilizadas en el Casino de Monte Carlo.
    - **Funcionamiento**: Utiliza sectores del cilindro ("tiers du cylindre", "voisins du zero", "orphelins") para determinar apuestas.
    - **Ventajas**: Cobertura estratégica de diferentes sectores físicos de la rueda.
    - **Desventajas**: Requiere adaptación constante y buen timing.

### Estrategias basadas en Ciencia y Física (Todas Inventadas)

24. **QuantumObserverStrategy (Física cuántica)**
    - **Descripción**: Basada en principios de la física cuántica como el principio de incertidumbre y el efecto del observador.
    - **Funcionamiento**: Modeliza estados cuánticos para cada número, con fases de superposición, entrelazamiento y colapso.
    - **Ventajas**: Adaptabilidad al "colapsar" probabilidades tras observaciones.
    - **Desventajas**: Alta complejidad conceptual y computacional.

25. **ChaosTheoryStrategy (Teoría del caos)**
    - **Descripción**: Implementa principios de sistemas caóticos deterministas, como el efecto mariposa.
    - **Funcionamiento**: Utiliza ecuaciones como el mapa logístico y el sistema de Lorenz para generar patrones aparentemente aleatorios pero deterministas.
    - **Ventajas**: Capacidad para identificar patrones emergentes en sistemas complejos.
    - **Desventajas**: Sensibilidad extrema a condiciones iniciales.

26. **StatisticalMechanicsStrategy (Mecánica estadística)**
    - **Descripción**: Aplica conceptos de termodinámica y mecánica estadística al comportamiento de los números.
    - **Funcionamiento**: Modela "estados de energía" y "fases" del sistema (ordenado, desordenado, crítico) con distribuciones de Maxwell-Boltzmann.
    - **Ventajas**: Enfoque sistemático para adaptarse a diferentes regímenes de comportamiento.
    - **Desventajas**: Requiere suficientes datos para construir distribuciones estadísticamente significativas.

## Notas Importantes

- Este simulador tiene fines exclusivamente educativos y de investigación.
- Todas las estrategias, incluso las "reales", están implementadas como modelos simplificados.
- Las estrategias "vetadas" no son necesariamente ilegales, pero algunos casinos pueden restringir su uso.
- Las estrategias científicas son representaciones conceptuales que aplican metáforas de campos científicos, no implementaciones rigurosas de estas teorías.
- El simulador demuestra que, a largo plazo, la expectativa matemática favorece a la casa independientemente de la estrategia utilizada.

## Resultados y Análisis

Después de ejecutar el simulador, obtendrás:

1. Un resumen detallado de cada estrategia con:
   - Probabilidad de éxito (porcentaje de sesiones con beneficio)
   - Tasa de victoria (porcentaje de tiradas ganadas)
   - Beneficio/Pérdida promedio
   - Estadísticas de terminación (bancarrota, máximo de tiradas, objetivo alcanzado)
   - Números más efectivos para cada estrategia

2. Gráficos comparativos guardados en el archivo especificado por `--output-plot`
