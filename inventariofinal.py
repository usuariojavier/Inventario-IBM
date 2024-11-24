import unicodedata

def quitar_tildes(texto):
    # Normaliza el texto (descompone los caracteres acentuados)
    normalizado = unicodedata.normalize('NFKD', texto)
    # Filtra los caracteres que no son ASCII
    return ''.join(c for c in normalizado if not unicodedata.combining(c))

class Producto:                                                 # CLASE PRODUCTO
    def __init__(self, nombre, categoria, precio, cantidad):   # Normalizamos nombre y categoría al crear el producto
        self.__nombre = quitar_tildes(nombre.lower().strip())
        self.__categoria = quitar_tildes(categoria.lower().strip())
        self.__precio = precio
        self.__cantidad = cantidad

    @property
    def nombre(self):
        return self.__nombre            #  nombre  privado
    
    @property
    def categoria(self):
        return self.__categoria          #  categoría  privada
    
    @property
    def precio(self):
        return self.__precio               #  precio privado
    
    @property
    def cantidad(self):
        return self.__cantidad             #  cantidad  privada
    
    @nombre.setter          
    def nombre(self, nombre):               # Normalizar  nombre al actualizarlo 
        self.__nombre = quitar_tildes(nombre.lower().strip())
    
    @categoria.setter
    def categoria(self, categoria):          # Normalizar  categoría al actualizarla
        self.__categoria = quitar_tildes(categoria.lower().strip())
    
    @precio.setter
    def precio(self, precio):                # Normalizar  precio al actualizarlo
        self.__precio = precio
    
    @cantidad.setter
    def cantidad(self, cantidad):            # Normalizar cantidad al actualizarla
        self.__cantidad = cantidad

    def __str__(self):   
        return f"Nombre: {self.nombre.title()}, Categoría: {self.categoria.title()}, Precio: {self.precio}, Cantidad: {self.cantidad}"

    def __eq__(self, otro):
        if not isinstance(otro, Producto):        # Verificar si el otro objeto es un Producto
            return False
        return self.nombre == otro.nombre

class Inventario:                  ##################   CLASE INVENTARIO ###################
    def __init__(self):        
        self.__productos = []             

    def agregar_producto(self, nuevo_producto):                   ## METODO AGREGAR PRODUCTO ##
        if nuevo_producto in self.__productos:
            return False
        self.__productos.append(nuevo_producto)
        return True    

    def actualizar_producto(self, nombre, nuevo_precio=None, nueva_cantidad=None):      ## METODO ACTUALIZAR PRODUCTO ##
        nombre_normalizado = quitar_tildes(nombre.lower().strip())
        for producto in self.__productos:
            if producto.nombre == nombre_normalizado:                   # si el producto ya existe, actualiza sus atributos
                if nuevo_precio is not None:
                    producto.precio = nuevo_precio
                if nueva_cantidad is not None:
                    producto.cantidad = nueva_cantidad
                print("Producto actualizado.")
                return
        print("Producto no encontrado.")

    def eliminar_producto(self, nombre):                                      ## METODO ELIMINAR PRODUCTO ##
        nombre_normalizado = quitar_tildes(nombre.lower().strip())
        for producto in self.__productos:
            if producto.nombre == nombre_normalizado:
                self.__productos.remove(producto)
                print("Producto eliminado.")
                return
        print("Producto no encontrado.")

    def mostrar_inventario(self):                                       ## METODO MOSTRAR INVENTARIO ##
        if not self.__productos:
            print(" Inventario vacío.")
        else:
            for producto in self.__productos:
                print(producto)

    def buscar_producto(self, nombre):                                  ## METODO BUSCAR PRODUCTO ##
        nombre_normalizado = quitar_tildes(nombre.lower().strip())
        for producto in self.__productos:
            if producto.nombre == nombre_normalizado:
                print(producto)
                return
        print("Producto no encontrado.")

def validar_nombre(nombre):                                              ## METODO VALIDAR NOMBRE ##
    nombre_normalizado = quitar_tildes(nombre.strip())
    if len(nombre_normalizado) == 0:
        return False, "El nombre no puede estar vacío."
    if len(nombre_normalizado) < 3:
        return False, "El nombre debe tener al menos 3 caracteres."
    if not nombre_normalizado.replace(' ', '').isalpha(): 
        return False, "El nombre solo debe contener letras."
    return True, ""

def validar_categoria(categoria):                                       ## METODO VALIDAR CATEGORIA ##
    categoria_normalizada = quitar_tildes(categoria.strip())
    if len(categoria_normalizada) == 0:
        return False, "La categoria no puede estar vacía."
    if len(categoria_normalizada) < 3:
        return False, "La categoria debe tener al menos 3 caracteres."
    if not categoria_normalizada.replace(' ', '').isalpha(): 
        return False, "La categoria solo debe contener letras."
    return True, ""    

def menu():                    
    inventario = Inventario()
    while True:                                                         # mientras sea true...:
        print("\n---  INVENTARIO ---\n ")
        print("      Menú :\n")
        print("1. Añadir producto")
        print("2. Actualizar producto")
        print("3. Eliminar producto")
        print("4. Mostrar inventario")
        print("5. Buscar producto  ")
        print("6. Salir  \n")

        opcion = input("Elige una opción: ")

        if opcion == '1':                                                    ######### 1 AÑADIR  #########
            print("\n=== AÑADIR NUEVO PRODUCTO ===")
            while True:
                nombre = input("Ingresa nombre del producto: ")    
                nombre_valido, mensaje = validar_nombre(nombre)               # validar nombre
                if not nombre_valido:
                    print(f"Error: {mensaje}")
                    continue
                
                categoria = input("Ingresa categoría: ")                             
                categoria_valida, mensaje = validar_categoria(categoria)               # validar categoria
                if not categoria_valida:
                    print(f"Error: {mensaje}")
                    continue

                try:                                                               # validar precio y cantidad
                    precio = float(input("Ingresa precio: "))                   
                
                    if precio <= 0:                                               # precio debe ser mayor que 0
                        print("Error: El precio debe ser mayor que 0.")
                        continue
                    
                    cantidad = int(input("Ingresa cantidad: "))                  # cantidad debe ser mayor que 0
                    if cantidad <= 0:
                        print("Error: La cantidad debe ser mayor que 0.")
                        continue

                    producto = Producto(nombre, categoria, precio, cantidad)          # producto = Producto(nombre, categoria, precio, cantidad)
                    if inventario.agregar_producto(producto):
                        print(f"\nProducto '{nombre}' agregado !")
                    else:                                                                 
                        print(f"\nEl producto '{nombre}' ya existe en el inventario.")           # si el producto ya existe
                    break

                except ValueError:                                                         # si el precio o la cantidad no son numeros
                    print("Error: El precio y cantidad deben ser números válidos!!!")           
        
        elif opcion == '2':                                                   ############ 2 ACTUALIZAR ###########
            print("\n=== ACTUALIZAR PRODUCTO ===")
            nombre = input("Ingresa el nombre del producto a actualizar: ")
    
            try:
                nuevo_precio = float(input("Ingresa nuevo precio (Enter para mantener actual): ") or -1)   
                nueva_cantidad = int(input("Ingresa nueva cantidad (Enter para mantener actual): ") or -1)  
                precio_final = nuevo_precio if nuevo_precio >= 0 else None
                cantidad_final = nueva_cantidad if nueva_cantidad >= 0 else None
        
                if precio_final is None and cantidad_final is None:   # si no se ingresa ningun valor
                    print("No se realizaron cambios.")
                else:
                    inventario.actualizar_producto(nombre, precio_final, cantidad_final)  # actualizar
            
            except ValueError:
                print("Error: Los valores deben ser números válidos.")          

        elif opcion == '3':                                                ########    3 ELIMINAR    ########
            nombre = input("Que producto desea eliminar? : ")
            inventario.eliminar_producto(nombre)  

        elif opcion == '4':                                                ########## 4 MOSTRAR  ##########
            inventario.mostrar_inventario()

        elif opcion == '5':                                                   ########## 5 BUSCAR ##########
            nombre = input("Que producto desea buscar? : ")
            inventario.buscar_producto(nombre)
            
        elif opcion > '6' or  opcion < '1' or opcion == '':                   #  OPCION NO VALIDA
            print("Opcion no valida.\nElige una opcion entre 1 y 6.")
            continue

        elif opcion == '6':                                                    ##########3 6 SALIR      ########
            break

if __name__ == "__main__":
    menu()