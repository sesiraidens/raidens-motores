<div align="center">

<img src="https://sesiraidens.github.io/portifolio/assets/logo_color-aNRVU26Y.png" width="80">

# raidens-motores

Biblioteca completa de motores: DC, servo, passo, driver L298N e mecanum.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-d9333b?style=flat)
![Status](https://img.shields.io/badge/Status-Active-2ea043?style=flat)

</div>

---

## Sobre

O **raidens-motores** fornece classes para controle de todos os tipos de motores usados em robotica: DC, servo, passo e mecanum.

---

## Motores Disponiveis

### Motor DC

| Classe | Descricao |
|---|---|
| MotorDC | Motor DC individual |
| DriverL298N | Driver para 2 motores |

### Servo

| Classe | Descricao |
|---|---|
| ServoMotor | Servo SG90 angular |

### Motor de Passo

| Classe | Descricao |
|---|---|
| MotorPasso | 28BYJ-48 com ULN2003 |

### Mecanum

| Classe | Descricao |
|---|---|
| MecanumDriver | Rodas mecanum omnidirecionais |

---

## Uso

### Motor DC

`python
from src.motores import MotorDC

motor = MotorDC(nome="roda_esq", pin_velocidade=5, pin_direcao=2)
motor.forward(200)
motor.backward(150)
motor.stop()
motor.rampa(destino=255, passo=10)
`

### Driver L298N

`python
from src.motores import DriverL298N

driver = DriverL298N()
driver.frente(200)
driver.esquerda(150)
driver.direita(150)
driver.girar(90, velocidade=100)  # Gira 90 graus
driver.curva(raio=50)  # Curva com raio
driver.parar()
`

### Servo Motor

`python
from src.motores import ServoMotor

servo = ServoMotor(pin=11)
servo.mover(45)
servo.centro()
servo.suave(destino=90, passo=2, delay=0.02)
servo.varredura(inicio=0, fim=180, passo=5)
`

### Motor de Passo

`python
from src.motores import MotorPasso

motor = MotorPasso(pins=[8, 9, 10, 11])
motor.graus(90)  # Gira 90 graus
motor.revolucao()  # Uma volta completa
motor.posicao()  # Retorna posicao atual
`

### Mecanum

`python
from src.motores import MecanumDriver

mecanum = MecanumDriver()
mecanum.frente(200)
mecanum.esquerda(150)  # Movimento lateral
mecanum.girar(100)  # Rotacao no eixo
mecanum.mover(x=100, y=150, rotacao=50)  # Omnidirecional
`

---

## Funcionalidades

### Rampa de Aceleracao

`python
motor.rampa(destino=255, passo=10, delay=0.01)
`

### Giro por Angulo

`python
driver.girar(angulo=90, velocidade=100)
`

### Curva com Raio

`python
driver.curva(raio=50, velocidade=150)
`

### Varredura de Servo

`python
servo.varredura(inicio=0, fim=180, passo=5, delay=0.05)
`

---

## Equipe

**RAIDENS - SESI Aluminio 192**

Desenvolvido para uso interno da equipe. Licenciado sob MIT.