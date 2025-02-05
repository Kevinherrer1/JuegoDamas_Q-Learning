# **Agente de Damas con Aprendizaje por Refuerzo (Q-Learning)**  

Este proyecto implementa un agente autónomo capaz de jugar Damas en un tablero reducido de 4x4, utilizando el algoritmo **Q-Learning** para mejorar su rendimiento a medida que juega más partidas.  

## **Características del Proyecto**  
- Implementación del juego de Damas en Python.  
- Uso de **Q-Learning** para el aprendizaje del agente.  
- Almacenamiento del conocimiento en `q_table.pkl`.  
- Interfaz gráfica con **Pygame** para la visualización del juego.  
- Registro de partidas para analizar la evolución del agente.  

## **Requisitos**  
Antes de ejecutar el código, asegúrate de tener instaladas las siguientes bibliotecas:  

```bash
pip install numpy pygame pickle5
```
## **Ejecución del Juego**
Para iniciar una partida, ejecuta el siguiente comando en la terminal:
```bash
python main.py
```

## Funcionamiento del Algoritmo

El agente aprende utilizando la ecuación de actualización de Q-Learning:

\[
Q(S, A) = Q(S, A) + \alpha [R + \gamma \max Q(S', A') - Q(S, A)]
\]
Donde:

- **S** = Estado actual del tablero.
- **A** = Acción tomada.
- **R** = Recompensa obtenida por la acción.
- **S'** = Nuevo estado después de la acción.
- **α** = Tasa de aprendizaje.
- **γ** = Factor de descuento para valorar futuras recompensas.

Cada partida jugada por el agente queda registrada en la tabla Q (`q_table.pkl`), permitiéndole mejorar sus decisiones en futuras partidas.



## Resultados del Entrenamiento

Tras jugar 23 partidas contra un humano, se observó una evolución en la eficiencia del agente. Inicialmente, no lograba capturar piezas ni ejecutar estrategias efectivas. Sin embargo, con el tiempo comenzó a mejorar, logrando capturar piezas, promocionar fichas a reina y esquivar ataques. En la partida 23, el agente logró su primera victoria legítima, demostrando un aprendizaje efectivo.

## Autores

Kevin Herrera  
Proyecto desarrollado como parte de un estudio sobre Aprendizaje por Refuerzo en juegos de mesa.


