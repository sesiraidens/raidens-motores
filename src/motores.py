"""
Biblioteca de motores para robotica.

Contem drivers e classes para controle de todos os
tipos de motores usados nos robos da RAIDENS.
"""
import time
import math


class MotorBase:
    """
    Classe base para todos os motores.
    
    Fornece funcionalidade comum como rampa e limites.
    """
    
    def __init__(self, nome):
        self.nome = nome
        self.velocidade_atual = 0
        self.velocidade_maxima = 255
        self.velocidade_minima = -255
        self.reativo = True
        
    def forward(self, velocidade=255):
        """Move para frente."""
        raise NotImplementedError
        
    def backward(self, velocidade=255):
        """Move para tras."""
        raise NotImplementedError
        
    def stop(self):
        """Para o motor."""
        self.velocidade_atual = 0
        
    def brake(self):
        """Frenagem ativa."""
        self.velocidade_atual = 0
        
    def set_velocidade(self, velocidade):
        """
        Define velocidade (-255 a +255).
        
        Positivo = frente, negativo = tras.
        """
        velocidade = max(self.velocidade_minima, min(self.velocidade_maxima, velocidade))
        
        if velocidade >= 0:
            self.forward(velocidade)
        else:
            self.backward(abs(velocidade))
            
    def rampa(self, destino, passo=10, delay=0.01):
        """
        Rampa suave de velocidade.
        
        Args:
            destino: Velocidade final
            passo: Incremento por passo
            delay: Tempo entre passos
        """
        if self.velocidade_atual < destino:
            while self.velocidade_atual < destino:
                nova = min(self.velocidade_atual + passo, destino)
                self.set_velocidade(nova)
                time.sleep(delay)
        else:
            while self.velocidade_atual > destino:
                nova = max(self.velocidade_atual - passo, destino)
                self.set_velocidade(nova)
                time.sleep(delay)


class MotorDC(MotorBase):
    """
    Motor DC com controle de velocidade via PWM.
    """
    
    def __init__(self, nome="MotorDC", pin_velocidade=5, pin_direcao=2):
        super().__init__(nome)
        self.pin_velocidade = pin_velocidade
        self.pin_direcao = pin_direcao
        
    def forward(self, velocidade=255):
        """Move para frente."""
        self.velocidade_atual = max(0, min(255, velocidade))
        print(f"[{self.nome}] Forward: {self.velocidade_atual}")
        
    def backward(self, velocidade=255):
        """Move para tras."""
        self.velocidade_atual = max(0, min(255, velocidade))
        print(f"[{self.nome}] Backward: {self.velocidade_atual}")
        
    def stop(self):
        """Para o motor."""
        self.velocidade_atual = 0
        print(f"[{self.nome}] Stop")
        
    def brake(self):
        """Frenagem ativa."""
        self.velocidade_atual = 0
        print(f"[{self.nome}] Brake")


class DriverL298N:
    """
    Driver L298N para controle de dois motores DC.
    
    Permite velocidade e direcao independentes.
    """
    
    def __init__(self, nome="L298N"):
        self.nome = nome
        self.motor_esquerdo = MotorDC("Esquerdo")
        self.motor_direito = MotorDC("Direito")
        
    def mover(self, esquerdo, direito):
        """
        Define velocidade de cada motor.
        
        Args:
            esquerdo: -255 a +255
            direito: -255 a +255
        """
        self.motor_esquerdo.set_velocidade(esquerdo)
        self.motor_direito.set_velocidade(direito)
        
    def frente(self, velocidade=255):
        """Move ambos para frente."""
        self.mover(velocidade, velocidade)
        
    def tras(self, velocidade=255):
        """Move ambos para tras."""
        self.mover(-velocidade, -velocidade)
        
    def esquerda(self, velocidade=255):
        """Gira para esquerda (diferencial)."""
        self.mover(-velocidade, velocidade)
        
    def direita(self, velocidade=255):
        """Gira para direita (diferencial)."""
        self.mover(velocidade, -velocidade)
        
    def girar(self, angulo, velocidade=100):
        """
        Gira angulo especifico.
        
        Args:
            angulo: Graus para girar (positivo = horario)
            velocidade: Velocidade do giro
        """
        tempo_giro = abs(angulo) / 90.0
        
        if angulo > 0:
            self.direita(velocidade)
        else:
            self.esquerda(velocidade)
            
        time.sleep(tempo_giro)
        self.parar()
        
    def parar(self):
        """Para ambos os motores."""
        self.mover(0, 0)
        
    def frenagem(self):
        """Frenagem ativa nos dois motores."""
        self.motor_esquerdo.brake()
        self.motor_direito.brake()
        
    def curva(self, raio, velocidade=150):
        """
        Executa curva com raio especifico.
        
        Args:
            raio: Raio da curva (positivo = esquerda)
            velocidade: Velocidade base
        """
        if raio == 0:
            self.girar(90, velocidade)
            return
            
        if raio > 0:
            vel_interno = velocidade * 0.5
            vel_externo = velocidade
        else:
            vel_interno = velocidade
            vel_externo = velocidade * 0.5
            raio = abs(raio)
            
        self.mover(int(vel_interno), int(vel_externo))
        
    def aceleracao(self, destino, passo=10, delay=0.01):
        """
        Aceleracao suave para destino.
        
        Args:
            destino: Velocidade final
            passo: Incremento por passo
            delay: Tempo entre passos
        """
        self.motor_esquerdo.rampa(destino, passo, delay)
        self.motor_direito.rampa(destino, passo, delay)


class ServoMotor(MotorBase):
    """
    Servo motor SG90 para controle angular.
    """
    
    def __init__(self, nome="Servo", pin=11, angulo_min=0, angulo_max=180):
        super().__init__(nome)
        self.pin = pin
        self.angulo_atual = 90
        self.angulo_min = angulo_min
        self.angulo_max = angulo_max
        
    def forward(self, velocidade=90):
        """Move para angulo especifico."""
        self.mover(velocidade)
        
    def backward(self, velocidade=90):
        """Move para angulo oposto."""
        self.mover(180 - velocidade)
        
    def mover(self, angulo):
        """
        Move servo para angulo.
        
        Args:
            angulo: 0 a 180 graus
        """
        self.angulo_atual = max(self.angulo_min, min(self.angulo_max, angulo))
        print(f"[{self.nome}] Angulo: {self.angulo_atual}")
        
    def centro(self):
        """Move para centro (90)."""
        self.mover(90)
        
    def esquerda(self):
        """Move para extrema esquerda."""
        self.mover(self.angulo_min)
        
    def direita(self):
        """Move para extrema direita."""
        self.mover(self.angulo_max)
        
    def incrementar(self, angulo=5):
        """Incrementa angulo."""
        self.mover(self.angulo_atual + angulo)
        
    def decrementar(self, angulo=5):
        """Decrementa angulo."""
        self.mover(self.angulo_atual - angulo)
        
    def suave(self, destino, passo=1, delay=0.01):
        """
        Movimento suave ate destino.
        
        Args:
            destino: Angulo final
            passo: Incremento por passo
            delay: Tempo entre passos
        """
        if self.angulo_atual < destino:
            while self.angulo_atual < destino:
                self.incrementar(passo)
                time.sleep(delay)
        else:
            while self.angulo_atual > destino:
                self.decrementar(passo)
                time.sleep(delay)
                
    def varredura(self, inicio=0, fim=180, passo=5, delay=0.05):
        """
        Executa varredura angular.
        
        Args:
            inicio: Angulo inicial
            fim: Angulo final
            passo: Incremento
            delay: Tempo entre passos
        """
        if inicio < fim:
            for angulo in range(inicio, fim + 1, passo):
                self.mover(angulo)
                time.sleep(delay)
        else:
            for angulo in range(inicio, fim - 1, -passo):
                self.mover(angulo)
                time.sleep(delay)


class MotorPasso(MotorBase):
    """
    Motor de passo 28BYJ-48 com ULN2003.
    """
    
    SEQUENCIA = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    
    PASSOS_POR_REVOLUCAO = 2048
    
    def __init__(self, nome="MotorPasso", pins=None):
        super().__init__(nome)
        self.pins = pins or [8, 9, 10, 11]
        self.posicao_atual = 0
        
    def forward(self, velocidade=1):
        """Executa um passo para frente."""
        self.passo(1)
        
    def backward(self, velocidade=1):
        """Executa um passo para tras."""
        self.passo(-1)
        
    def passo(self, direcao=1, delay=0.002):
        """
        Executa um passo.
        
        Args:
            direcao: 1 = horario, -1 = anti-horario
            delay: Tempo entre passos
        """
        for sequencia in self.SEQUENCIA:
            print(f"  Passo: {sequencia}")
            time.sleep(delay)
            
        self.posicao_atual += direcao
        
    def mover_passos(self, num_passos, direcao=1, delay=0.002):
        """Move numero especifico de passos."""
        for _ in range(abs(num_passos)):
            self.passo(direcao, delay)
            
    def revolucao(self, direcao=1):
        """Executa uma revolucao completa."""
        self.mover_passos(self.PASSOS_POR_REVOLUCAO, direcao)
        
    def graus(self, angulo, direcao=1):
        """Move angulo especifico em graus."""
        passos = int(self.PASSOS_POR_REVOLUCAO * angulo / 360)
        self.mover_passos(passos, direcao)
        
    def posicao(self):
        """Retorna posicao em passos."""
        return self.posicao_atual
        
    def reset(self):
        """Reseta posicao."""
        self.posicao_atual = 0


class MecanumDriver:
    """
    Driver para robos com rodas mecanum.
    
    Permite movimento omnidirecional.
    """
    
    def __init__(self):
        self.motores = {
            "frontal_esq": MotorDC("FE"),
            "frontal_dir": MotorDC("FD"),
            "traseira_esq": MotorDC("TE"),
            "traseira_dir": MotorDC("TD")
        }
        
    def mover(self, x, y, rotacao=0):
        """
        Movimento omnidirecional.
        
        Args:
            x: Velocidade lateral (-255 a +255)
            y: Velocidade longitudinal (-255 a +255)
            rotacao: Velocidade de rotacao (-255 a +255)
        """
        v1 = y + x + rotacao
        v2 = y - x - rotacao
        v3 = y - x + rotacao
        v4 = y + x - rotacao
        
        max_val = max(abs(v1), abs(v2), abs(v3), abs(v4))
        
        if max_val > 255:
            v1 = int(v1 * 255 / max_val)
            v2 = int(v2 * 255 / max_val)
            v3 = int(v3 * 255 / max_val)
            v4 = int(v4 * 255 / max_val)
            
        self.motores["frontal_esq"].set_velocidade(v1)
        self.motores["frontal_dir"].set_velocidade(v2)
        self.motores["traseira_esq"].set_velocidade(v3)
        self.motores["traseira_dir"].set_velocidade(v4)
        
    def frente(self, velocidade=255):
        """Move para frente."""
        self.mover(0, velocidade, 0)
        
    def tras(self, velocidade=255):
        """Move para tras."""
        self.mover(0, -velocidade, 0)
        
    def esquerda(self, velocidade=255):
        """Move para esquerda."""
        self.mover(-velocidade, 0, 0)
        
    def direita(self, velocidade=255):
        """Move para direita."""
        self.mover(velocidade, 0, 0)
        
    def girar(self, velocidade=255):
        """Gira no proprio eixo."""
        self.mover(0, 0, velocidade)
        
    def parar(self):
        """Para todos os motores."""
        self.mover(0, 0, 0)
