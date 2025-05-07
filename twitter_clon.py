# Lista donde guarda los tweets
tweets = []

# Funcion para mostrar el menu
def mostrar_menu():
    print("\n--- Mini Twitter ---")
    print("1. Escribir un tweet")
    print("2. Ver tweets")
    print("3. Salir")
    
# Bucle principal
while True:
    mostrar_menu()
    opcion = input("Selecciona una opcion: ")
    
    if opcion == "1":
        tweet = input("Escribe tu tweet: ")
        tweets.append(tweet)
        print("Tweet Publicado!")
    elif opcion == "2":
        print("\n--- Tweets ---")
        for i, t in enumerate(tweets, 1):
            print(f"{i}. {t}")
    elif opcion == "3":
        print("Saliendo...")
        break
    else:
        print("Opcion no valida. Intenta de nuevo.")