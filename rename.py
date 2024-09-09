import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RenameHandler(FileSystemEventHandler):
    def __init__(self):
        self.is_renaming = False

    def on_moved(self, event):
        if self.is_renaming:
            return

        if not event.is_directory and event.dest_path.startswith(path_to_watch):
            directory_path = os.path.dirname(event.dest_path)
            base_name = os.path.splitext(os.path.basename(event.dest_path))[0]
            extension = os.path.splitext(os.path.basename(event.dest_path))[1]
            
            files = sorted([f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))])

            if "_" not in os.path.basename(event.dest_path):
                self.is_renaming = True
                for index, file in enumerate(files):
                    if file == os.path.basename(event.dest_path):
                        continue
                    new_name = f"{base_name}_{index}{extension}"
                    os.rename(os.path.join(directory_path, file), os.path.join(directory_path, new_name))
                self.is_renaming = False

                print(f"Файлы в {directory_path} были переименованы.")

if __name__ == "__main__":
    path_to_watch = input("Напиши путь директории: ")

    event_handler = RenameHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
