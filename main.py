import yt_dlp
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import shutil
import os, sys

def make_audio(text, ext):
    # text와 ext를 받아서 실제 파일 생성했다고 가정
    # 파일 이름을 반환
    global ffmpeg_path
    URLS = f'{text}'

    ydl_opts = {
        'format': f'{ext}/bestaudio/best',
        'ffmpeg_location': ffmpeg_path,
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg

            'key': 'FFmpegExtractAudio',
            'preferredcodec': f'{ext}',
        }],
        'outtmpl': f'{os.path.abspath(".")}/tmp/%(title)s.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        #error_code = ydl.download(URLS)
        info = ydl.extract_info(URLS, download=True)
        file_path = info["requested_downloads"][0]["filepath"]

    return file_path

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Audio Downloader")
        self.geometry("400x200")

        # 상단: 텍스트 입력 필드
        self.entry = tk.Entry(self, width=40)
        self.entry.pack(pady=10)

        # 중단: 확장자 드롭다운 + 실행 버튼
        frame_mid = tk.Frame(self)
        frame_mid.pack(pady=10)

        self.ext_var = tk.StringVar(value="mp3")
        self.combo = ttk.Combobox(frame_mid, textvariable=self.ext_var, values=["mp3", "wav", "ogg"], width=10, state="readonly")
        self.combo.pack(side="left", padx=5)

        self.run_btn = tk.Button(frame_mid, text="실행", command=self.run_make_audio)
        self.run_btn.pack(side="left", padx=5)

        # 하단: 파일 이름 표시 + 저장 버튼
        frame_bottom = tk.Frame(self)
        frame_bottom.pack(pady=20)

        self.file_var = tk.StringVar(value="생성된 파일 없음")
        self.label = tk.Label(frame_bottom, textvariable=self.file_var, width=25, anchor="w")
        self.label.pack(side="left", padx=5)

        self.save_btn = tk.Button(frame_bottom, text="저장", command=self.save_file)
        self.save_btn.pack(side="left", padx=5)

        # 내부 상태
        self.generated_file = None

    def run_make_audio(self):
        text = self.entry.get().strip()
        ext = self.ext_var.get()
        if not text:
            messagebox.showwarning("입력 필요", "텍스트를 입력하세요.")
            return
        # 오디오 생성 함수 호출
        self.generated_file = make_audio(text, ext)
        self.file_var.set(self.generated_file)

    def save_file(self):
        if not self.generated_file:
            messagebox.showwarning("저장 불가", "먼저 파일을 생성하세요.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=f".{self.ext_var.get()}",
                                                 filetypes=[("Audio Files", f"*.{self.ext_var.get()}"), ("All Files", "*.*")],
                                                 initialfile=self.generated_file)
        if save_path:
            shutil.copy(self.generated_file, save_path)
            messagebox.showinfo("저장 완료", f"{save_path} 저장됨")


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):  # PyInstaller로 빌드된 경우
        base_path = sys._MEIPASS
    else:  # 개발 환경
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


ffmpeg_path = ''
ffplay_path = ''
ffprobe_path = ''

if __name__ == "__main__":
    ffmpeg_path = resource_path(os.path.join("ffmpeg", "ffmpeg.exe"))
    ffplay_path = resource_path(os.path.join("ffmpeg", "ffplay.exe"))
    ffprobe_path = resource_path(os.path.join("ffmpeg", "ffprobe.exe"))

    app = App()
    app.mainloop()


