import asyncio
import unittest
from playlist_module import Song, Playlist


class TestPlaylist(unittest.IsolatedAsyncioTestCase):

    async def test_add_song(self):
        playlist = Playlist()
        song = Song("Song Title", 3.5)
        await playlist.add_song(song)
        self.assertEqual(playlist.head, playlist.tail)
        self.assertEqual(playlist.head.song.title, "Song Title")
        self.assertEqual(playlist.head.song.duration, 3.5)

    async def test_play(self):
        playlist = Playlist()
        song = Song("Song 1", 3.5)
        await playlist.add_song(song)
        song = Song("Song 2", 2.0)
        await playlist.add_song(song)
        await playlist.play()
        self.assertTrue(playlist.is_playing)
        await asyncio.sleep(6.0)
        self.assertFalse(playlist.is_playing)

    async def test_pause(self):
        playlist = Playlist()
        song = Song("Song 1", 3.5)
        await playlist.add_song(song)
        song = Song("Song 2", 2.0)
        await playlist.add_song(song)
        await playlist.play()
        await asyncio.sleep(1.0)
        await playlist.pause()
        self.assertFalse(playlist.is_playing)
        await asyncio.sleep(2.0)
        self.assertFalse(playlist.is_playing)

    async def test_next_song(self):
        playlist = Playlist()
        song = Song("Song 1", 3.5)
        await playlist.add_song(song)
        song = Song("Song 2", 2.0)
        await playlist.add_song(song)
        await playlist.play()
        self.assertEqual(playlist.current_song.song.title, "Song 1")
        await playlist.next_song()
        self.assertEqual(playlist.current_song.song.title, "Song 2")
        await asyncio.sleep(2.5)
        self.assertFalse(playlist.is_playing)

    async def test_prev_song(self):
        playlist = Playlist()
        song = Song("Song 1", 3.5)
        await playlist.add_song(song)
        song = Song("Song 2", 2.0)
        await playlist.add_song(song)
        await playlist.play()
        await playlist.next_song()
        self.assertEqual(playlist.current_song.song.title, "Song 2")
        await playlist.prev_song()
        self.assertEqual(playlist.current_song.song.title, "Song 1")
        await asyncio.sleep(4.5)
        self.assertFalse(playlist.is_playing)


if __name__ == "__main__":
    unittest.main()
