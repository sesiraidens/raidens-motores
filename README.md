<div align="center">

<img src="https://sesiraidens.github.io/portifolio/assets/logo_color-aNRVU26Y.png" alt="Logo RAIDENS" width="140">

# raidens-motores

**Controle de motores DC, servo, passo, driver L298N e rodas mecanum em Python**

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Sem dependências](https://img.shields.io/badge/depend%C3%AAncias-nenhuma-2EA043?style=flat-square)
![Licença MIT](https://img.shields.io/badge/Licen%C3%A7a-MIT-D9333B?style=flat-square)

[Sobre](#sobre) · [Instalação](#instalação) · [Motores](#motores-disponíveis) · [Uso](#uso)

</div>

---

## Sobre

O **raidens-motores** concentra tudo o que movimenta um robô da RAIDENS. As classes cuidam dos detalhes chatos (limitar o PWM entre 0 e 255, fazer rampa de aceleração, converter graus em passos) para que o código do robô fale em termos de *frente*, *girar 90°* e *curva com raio de 50*.

A saída é simulada no terminal, o que permite validar a sequência de movimentos antes de ligar os motores de verdade.

## Instalação

```bash
git clone https://github.com/sesiraidens/raidens-motores.git
cd raidens-motores
```

Requer apenas Python 3.8 ou superior. Rode os scripts a partir da raiz do repositório.

## Motores disponíveis

| Classe | Hardware | Destaques |
|---|---|---|
| `MotorDC` | Motor DC com PWM | `forward`, `backward`, `brake`, `rampa` |
| `DriverL298N` | Ponte H para 2 motores | `frente`, `girar(ângulo)`, `curva(raio)`, `aceleracao` |
| `ServoMotor` | Servo SG90 | `mover`, `suave`, `varredura` |
| `MotorPasso` | 28BYJ-48 com ULN2003 | `graus`, `revolucao`, `posicao` |
| `MecanumDriver` | 4 rodas mecanum | Movimento lateral e omnidirecional |

## Uso

### Motor DC e driver L298N

```python
from src.motores import MotorDC, DriverL298N

motor = MotorDC(nome="roda_esq", pin_velocidade=5, pin_direcao=2)
motor.forward(200)
motor.rampa(destino=255, passo=10)    # acelera aos poucos
motor.stop()

driver = DriverL298N()
driver.frente(200)
driver.girar(90, velocidade=100)      # gira 90 graus
driver.curva(raio=50, velocidade=150)
driver.parar()
```

### Servo

```python
from src.motores import ServoMotor

servo = ServoMotor(pin=11)
servo.mover(45)
servo.suave(destino=90, passo=2, delay=0.02)
servo.varredura(inicio=0, fim=180, passo=5)
```

### Motor de passo

```python
from src.motores import MotorPasso

passo = MotorPasso(pins=[8, 9, 10, 11])
passo.graus(90)
passo.revolucao()
passo.posicao()
```

### Mecanum

```python
from src.motores import MecanumDriver

mecanum = MecanumDriver()
mecanum.esquerda(150)                     # desliza para o lado
mecanum.mover(x=100, y=150, rotacao=50)   # qualquer direção
mecanum.parar()
```

## Estrutura

```text
raidens-motores/
└── src/
    └── motores.py   # MotorBase e todas as classes de motor
```

## Ecossistema RAIDENS

Este repositório faz parte de um conjunto de bibliotecas da equipe. Elas usam os mesmos nomes de classes e convenções, então o que você aprende em uma serve nas outras.

| Repositório | Para quê |
|---|---|
| [`raidens-python`](https://github.com/sesiraidens/raidens-python) | Biblioteca principal em Python: sensores, motores e robôs prontos (seguidor, parede, resgate) |
| [`raidens-arduino`](https://github.com/sesiraidens/raidens-arduino) | As mesmas abstrações em C++ para rodar direto no Arduino |
| [`raidens-sensores`](https://github.com/sesiraidens/raidens-sensores) | Catálogo completo de sensores com calibração e filtragem |
| [`raidens-pid`](https://github.com/sesiraidens/raidens-pid) | Controladores PID, PID avançado, cascata e sintonia Ziegler-Nichols |
| [`raidens-opencv`](https://github.com/sesiraidens/raidens-opencv) | Visão computacional: cores, linhas e navegação por câmera |
| [`raidens-lab`](https://github.com/sesiraidens/raidens-lab) | Calibração interativa de cores em HSV e LAB |
| [`raidens-obr`](https://github.com/sesiraidens/raidens-obr) | Robô completo para a OBR, integrando sensores, motores e missões |
| [`raidens-electronics`](https://github.com/sesiraidens/raidens-electronics) | Cálculos e modelos de componentes eletrônicos |
| [`raidens-3d`](https://github.com/sesiraidens/raidens-3d) | Peças 3D paramétricas geradas em OpenSCAD |
| [`raidens-ros`](https://github.com/sesiraidens/raidens-ros) | Estrutura de nodes e tópicos ROS 2 |
| [`raidens-snippets`](https://github.com/sesiraidens/raidens-snippets) | Trechos de código prontos para copiar e colar |

---

<div align="center">

<img src="https://sesiraidens.github.io/portifolio/assets/logo_color-aNRVU26Y.png" alt="Logo RAIDENS" width="56">

**Equipe RAIDENS** · SESI 192 Alumínio/SP

[![Email](https://img.shields.io/badge/Email-sesiraidens%40gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:sesiraidens@gmail.com)
[![Linktree](https://img.shields.io/badge/Linktree-sesiraidens-39E06B?style=flat-square&logo=linktree&logoColor=white)](https://linktr.ee/sesiraidens)
[![GitHub](https://img.shields.io/badge/GitHub-sesiraidens-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/sesiraidens)

<sub>Desenvolvido pela equipe RAIDENS para fins educacionais. Licenciado sob MIT.</sub>

</div>





