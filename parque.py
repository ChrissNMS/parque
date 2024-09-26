from datetime import datetime

# Clase Visitante
class Visitante:
    def __init__(self, nombre, edad, altura, dinero):
        self.nombre = nombre
        self.edad = edad
        self.altura = altura
        self.dinero = dinero
        self.tickets = []
        self.cola_actual = None
    
    def comprar_ticket(self, atraccion):
        if self.dinero >= atraccion.precio:
            self.dinero -= atraccion.precio
            ticket = Ticket(len(self.tickets) + 1, atraccion.nombre, atraccion.precio, datetime.now())
            self.tickets.append(ticket)
            print(f"{self.nombre} compró un ticket para la atracción {atraccion.nombre}")
        else:
            print("No tienes suficiente dinero para comprar este ticket.")

    def entregar_ticket(self, atraccion):
        for ticket in self.tickets:
            if ticket.atraccion == atraccion.nombre:
                self.tickets.remove(ticket)
                print(f"{self.nombre} entregó su ticket para la atracción {atraccion.nombre}")
                return
        print("No tienes un ticket para esta atracción.")

    def hacer_cola(self, atraccion):
        if self.cola_actual != atraccion:
            if self.cola_actual is not None:
                self.cola_actual.cola.remove(self)
                print(f"{self.nombre} dejó la cola de {self.cola_actual.nombre}")
            self.cola_actual = atraccion
            atraccion.cola.append(self)
            print(f"{self.nombre} se unió a la cola de {atraccion.nombre}")
        else:
            print(f"{self.nombre} ya está en la cola de {atraccion.nombre}")

# Clase Atraccion
class Atraccion:
    def __init__(self, nombre, capacidad, duracion, precio):
        self.nombre = nombre
        self.capacidad = capacidad
        self.duracion = duracion
        self.precio = precio
        self.estado = "activo"
        self.cola = []

    def iniciar_ronda(self):
        if self.estado == "activo" and len(self.cola) > 0:
            visitantes = self.cola[:self.capacidad]
            self.cola = self.cola[self.capacidad:]
            print(f"La ronda de {self.nombre} ha iniciado con {len(visitantes)} visitantes.")
            for visitante in visitantes:
                visitante.entregar_ticket(self)
        else:
            print("La atracción no está activa o no hay suficientes visitantes en la cola.")

    def comenzar_mantenimiento(self):
        self.estado = "fuera de servicio"
        print(f"La atracción {self.nombre} está en mantenimiento.")

    def finalizar_mantenimiento(self):
        self.estado = "activo"
        print(f"La atracción {self.nombre} está activa de nuevo.")

# Clase Ticket
class Ticket:
    def __init__(self, numero, atraccion, precio, fecha_compra):
        self.numero = numero
        self.atraccion = atraccion
        self.precio = precio
        self.fecha_compra = fecha_compra

# Clase Parque
class Parque:
    def __init__(self, nombre):
        self.nombre = nombre
        self.juegos = []
        self.ventas = []

    def agregar_atraccion(self, atraccion):
        self.juegos.append(atraccion)
    
    def consultar_juegos_activos(self):
        activos = [juego.nombre for juego in self.juegos if juego.estado == "activo"]
        print(f"Atracciones activas: {', '.join(activos)}")
        return activos

    def cobrar_ticket(self, visitante, atraccion):
        visitante.comprar_ticket(atraccion)
        self.ventas.append((atraccion.nombre, atraccion.precio))

    def resumen_de_ventas(self, dia):
        total_dinero = 0
        resumen = {}
        for venta in self.ventas:
            if venta[0] not in resumen:
                resumen[venta[0]] = 0
            resumen[venta[0]] += venta[1]
            total_dinero += venta[1]
        print(f"Resumen de ventas para el día {dia}:")
        for atraccion, total in resumen.items():
            print(f"Atracción: {atraccion} - Recaudado: ${total}")
        print(f"Total ingresos del día: ${total_dinero}")

# Clase AtraccionInfantil (heredada de Atraccion)
class AtraccionInfantil(Atraccion):
    def verificar_restricciones(self, visitante):
        if visitante.edad <= 10:
            return True
        else:
            print("Solo para niños de 10 años o menos.")
            return False

# Clase MontanaRusa (heredada de Atraccion)
class MontanaRusa(Atraccion):
    def __init__(self, nombre, capacidad, duracion, precio, velocidad_maxima, altura_maxima, extension):
        super().__init__(nombre, capacidad, duracion, precio)
        self.velocidad_maxima = velocidad_maxima
        self.altura_maxima = altura_maxima
        self.extension = extension

    def verificar_restricciones(self, visitante):
        if visitante.altura >= 140:
            return True
        else:
            print("Altura mínima de 140 cm requerida.")
            return False

# Clase VisitanteVIP (heredada de Visitante)
class VisitanteVIP(Visitante):
    def __init__(self, nombre, edad, altura, dinero):
        super().__init__(nombre, edad, altura, dinero)
        self.entradas_gratis = {}

    def comprar_ticket(self, atraccion):
        if self.entradas_gratis.get(atraccion.nombre, 0) < 2:
            self.entradas_gratis[atraccion.nombre] = self.entradas_gratis.get(atraccion.nombre, 0) + 1
            print(f"{self.nombre} tiene acceso VIP gratuito a {atraccion.nombre}.")
        else:
            super().comprar_ticket(atraccion)

# Script de prueba
parque = Parque("Parque Punta Arenas")
atraccion1 = AtraccionInfantil("Carrusel", 10, 5, 5)
atraccion2 = MontanaRusa("Velociraptor", 5, 15, 20, 80, 50, 300)

parque.agregar_atraccion(atraccion1)
parque.agregar_atraccion(atraccion2)

visitante1 = Visitante("Juan", 8, 120, 30)
visitante2 = Visitante("Ana", 12, 150, 50)
visitante_vip = VisitanteVIP("Christofer", 20, 170, 100)

# Pruebas
visitante1.comprar_ticket(atraccion1)
visitante2.comprar_ticket(atraccion2)
visitante_vip.comprar_ticket(atraccion2)

visitante1.hacer_cola(atraccion1)
visitante2.hacer_cola(atraccion2)
visitante_vip.hacer_cola(atraccion2)

atraccion1.iniciar_ronda()
atraccion2.iniciar_ronda()

parque.resumen_de_ventas("2024-09-26")
