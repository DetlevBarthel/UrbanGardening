# run_core_1 ist Anfangs 0. Deswegen ist core1_thread() angehalten => while not run_core_1 ist die Haltestelle in core1_thread
# core0_thread() zählt 5 Zahlen und setzt run_core_1 auf True. Dadurch wird core0_thread() am Ende blockiert und
# core1_thread() startet. Es liefert 2 Zahlen  und setzt run_core_1 wieder auf False
# jetzt geht es wieder von vorne los


from time import sleep
import _thread


def core0_thread():
    global run_core_1
    print(run_core_1)
    counter = 0
    while True:
        # print next 5 even numbers
        for loop in range(5):
            print(counter)
            counter += 2
            sleep(1)

        # signal core 1 to run
        run_core_1 = True

        # wait for core 1 to finish
        print("core 0 waiting")
        while run_core_1:
            pass


def core1_thread():
    global run_core_1
    counter = 1

    while True:

        # wait for core 0 to signal start
        print("core 1 waiting")
        while not run_core_1:
            pass

        # print next 3 odd numbers
        for loop in range(3):
            print(counter)
            counter += 2
            sleep(0.5)

        # signal core 0 code finished
        run_core_1 = False


# Global variable to send signals between threads
run_core_1 = False

second_thread = _thread.start_new_thread(core1_thread, ())
core0_thread()