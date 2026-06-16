from models.album import Album
class Storage:
    __albums:list[Album] = []

    def get_all_albums(self):
        return self.__albums
    
    def add_album(self, album:Album):
        self.__albums.append(album)

    def update_album(self, album:Album):
        for a in self.__albums:
            if a.id == album.id:
                a = album
                return a
        else:
            return None
    
    def delete_album(self, id):
        for a in self.__albums:
            if a.id == id:
                self.__albums.remove(a)
                break