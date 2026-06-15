from models.album import Album
class Storage:
    __albums:list[Album] = []

    def get_all_albums(self):
        return self.__albums
    
    def add_album(self, album:Album):
        self.__albums.append(album)