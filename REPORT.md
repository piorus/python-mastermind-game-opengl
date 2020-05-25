### Raport z projektu "Mastermind"
Wykonał: **Piotr Rusin**

Data wykonania: **01 Maj 2020 - 25 Maj 2020**

Projekt symuluje na komputerze rozgrywkę w grę planszową "Mastermind".

Do wykonania projektu zostało wykorzystane OpenGL 3.2 API (core-profile).
Kod prezentuje współczesne podejście do renderowania obiektów w 3D przy użyciu OpenGL'a.

Po startcie na ekranie pojawia się 12 rzędów po 4 białe kulki które reprezentują wszystkie
odpowiedzi z danej rozgrywki. Jedna z kulek w aktualnym wierszu będzie zawsze aktywna, umożliwiając zmianę wartości na liczbę z zakresu 1-6 (przyciski 1-6).
W każdym momencie można zmienić aktywną kulkę przy użyciu SPACJI. 

Po wybraniu wszystkich kulek z aktualnego rzędu gracz musi nacisnąć klawisz ENTER, co spowoduje sprawdzenie aktualnie wybranej kombinacji.

W przypadku gdy nie została odgadnięta właściwa kombinacja oraz nie doszło do końca gry, następuje weryfikacja wybranych wartości i wyświetlenie odpowiednich kulek jako odpowiedź zwrotna (feedback).

Zasady które określają ile kulek z odpowiedzi zwrotnej zostanie wyświetlonych oraz w jakim będą kolorze są dokładnie takie same jak w grze planszowej - każda kulka z odpowiedzi na właściwym miejscu dostaje odpowiednio po jednej kulce CZERWONEJ. Pozostałe z kulek które są w kombinacji, ale w odpowiedzi były na niewłaściym miejscu dostają odpowiednio po jednej kulce BIAŁEJ. Odpowiedź zwrotna nie zawsze będzie się składać z 4 kulek, w przypadku gdy liczba nie jest na właściwym miejscu ani nie jest w kombinacji, zostaje pominięta w odpowiedzi zwrotnej.

W przypadku gdy gracz odagł poprawną kombinację, na ekranie pojawia się informacja o wygraniu gry.

Po 12 nieudanych próbach odgadnięcia kombinacji, na ekranie pojawia się informacja o przegraniu gry.

Grę można w każdym momencie zrestartować wciskając klawisz R.

Po każdym restartcie (oraz przy startcie) losowane są aktywne reguły gry. 
Są dwie możliwości - albo będą poprawne, albo gra będzie w trybie OSZUST.
W każdym momencie rozgrywki można dokonać sprawdzenia reguł gry poprzez wciśnięcie klawisza O.
Po każdym sprawdzeniu trzeba zresetować grę.

Odnośnie punktu 5.2 z wymagań projektowych:
- lambda jest użyta w większości w klasie App::register_events() do pominięcia argumentu z callbacku który jest zawsze przekazywany przy przetwarzaniu zdarzeń.
- list comprehensions - klasa game.State
- wyjątki - klasa Shader