import asyncio


class Song:
    """Класс Song реализует тип данных "песня", которая содержит название и продолжительность этой песни"""

    def __init__(self, title: str, duration: float) -> None:
        """Конструктор типа данных Song

        :parameter:
        - title (str): название песни
        - duration (float): длительность песни в секундах
        """
        self.title = title
        self.duration = duration


class PlaylistNode:
    """
    Класс PlaylistNode, реализующий элемент двусвязного списка. Каждый элемент данной реализации содержит
    своё значение - песню, а также ссылки на следующий и предыдущий элементы списка воспроизведения
    """

    def __init__(self, song: Song) -> None:
        """Конструктор элемента списка воспроизведения

        :parameter:
        - song (Song): объект типа Song, который будет записан (сохранён)
        """
        self.song = song
        self.prev = None  # ссылка на следующую песню
        self.next = None  # ссылка на предыдущую песню


class Playlist:
    """
    Класс Playlist, реализующий основные методы работы с песней в списке воспроизведения,
    которые в свою очередь являются корутинами
    """

    def __init__(self) -> None:
        """Конструктор объекта типа Playlist

        :parameter:
        - head: ссылка на первую песню в списке воспроизведения
        - lock: объект блокировки для синхронизации доступа команд(методов) к списку воспроизведения
        """
        self.head = None  # ссылка на первую песню в списке воспроизведения
        self.tail = None  # ссылка на последнюю песню в списке воспроизведения
        self.current_song = None  # ссылка на текущую песню в списке воспроизведения
        self.is_playing = False  # флаг, показывающий проигрывается ли песня в текущий момент
        self.lock = asyncio.Lock()  # объект блокировки для синхронизации доступа к списку воспроизведения

    async def add_song(self, song) -> None:
        """Добавляет новую песню в конец списка воспроизведения

        :parameter:
        - song (Song): объект типа Song, который будет добавлен в список воспроизведения.
        """
        new_node = PlaylistNode(song)
        async with self.lock:  # учёт одновременного, конкурентного доступа
            if self.tail is None:
                self.head = new_node
                self.tail = new_node
            else:
                self.tail.next = new_node
                new_node.prev = self.tail
                self.tail = new_node

    async def play(self) -> None:
        """Начинает воспроизведение текущей песни или с первой песни в плейлисте,
        если текущий текущей песни не существует"""
        if not self.is_playing:
            self.is_playing = True
            if self.current_song is None:
                self.current_song = self.head
            loop = asyncio.get_event_loop()
            loop.create_task(self.play_song())

    async def play_song(self) -> None:
        """Воспроизводит текущую песню, и автоматически начинает проигрывание следующей песни в плейлисте"""
        while self.current_song is not None:
            print(f"Сейчас играет: {self.current_song.song.title}")
            await asyncio.sleep(self.current_song.song.duration)
            temp = self.current_song.song.duration
            async with self.lock:
                if self.current_song.next is None:
                    print(f"Доигрывается последняя песня в списке воспроизведения")
                    self.is_playing = False
                    await asyncio.sleep(temp)
                    """Если необходимо закольцевать плейлист, то вместо двух строчек сверху добавляется:
                    self.current_song = self.head
                    """
                else:
                    self.current_song = self.current_song.next
        self.is_playing = False

    async def pause(self) -> None:
        """Приостанавливает текущее воспроизведение"""
        self.is_playing = False

    async def next_song(self) -> None:
        """Останавливает текущее воспроизведение и начинает воспроизведение следующей песни"""
        async with self.lock:  # учёт одновременного, конкурентного доступа
            if self.current_song is not None:
                self.current_song = self.current_song.next
                await self.pause()
                await self.play()

    async def prev_song(self) -> None:
        """Останавливает текущее воспроизведение и начинает воспроизведение предыдущей песни"""
        async with self.lock:  # учёт одновременного, конкурентного доступа
            if self.current_song is not None:
                self.current_song = self.current_song.prev
                await self.pause()
                await self.play()
