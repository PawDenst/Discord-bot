# Discord-bot
Bot został przygotowany do działania na platformie Discord. Jest on umieszczony między innymi na serwerze zrzeszającym studentów Wydziału Elektroniki i Technik Informacyjnych. Całość kodu została napisana w języku programowania Python. <br />
Zadaniem bota jest wysyłanie planu zajęć spersonalizowanego względem każdego studenta oraz zbliżających się 	deadline'ów. Do tego wykorzystywane jest odpowiednio słowo klucz zajęcia/zajęcia dziś oraz terminarz. Oprócz tego bot posaida muzyczną funkcję, która pozwala na wspólne słuchanie muzyki przez wielu użytkowników jednocześnie. W implementacji wykorzsytano FFmpeg, który pozwala na bardzo szybką konwersję z jednego formatu do drugiego, zarówno wideo jak i audio. Dodatkowo wykorzystałem youtube-dl do pobierania różnej jakości filmów z youtube. <br />
Dostępne komendy (wpisywane po "!"): <br />
— **join** dołącza bota do kanału głosowego, <br />
— **leave** rozłącza bota z kanałem, <br />
— **play** pozwala zagrać dowolny utwór z platformy YouTube, <br />
— **pause** zatrzymuje obecnie odtwarzaną piosenkę,  <br />
— **resume** wznawia obecnie odtwarzaną piosenkę,  <br />
— **skip** przerywa obecnie graną piosenkę i odtwarza kolejną z kolejki, <br />
— **loop** zapętla obecnie odtwarzaną muzykę,  <br />
— **find** wyszukuje link do wpisanego tytułu,  <br />
— **view** wyświetla całą kolejkę,  <br />
— **clear** czyści całą kolejkę <br />
— **playingaudio** sprawdza, czy i jaka piosenka jest obecnie odtwarzana. <br />
Ponadto po użyciu komendy **memy** bot wysyła mema pochodzącego z reddita. Memy są _programistyczne_ i wysyłane są dopiero kiedy osiągną na owym portalu liczbę reakcji 500.
Wszystkie komendy wraz z ich opisem można podejrzeć przy użyicu komendy **help**.
