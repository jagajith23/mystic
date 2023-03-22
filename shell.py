import mystic

while True:
    try :
        text = input("mystic> ")

        if text == "": continue
        if text == "exit": break
        
        tokens, err = mystic.run("<main>", text)

        if err: print(err.as_string())
        else: print(tokens)
    except KeyboardInterrupt:
        break