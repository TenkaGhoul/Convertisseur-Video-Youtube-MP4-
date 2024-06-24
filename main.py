from pytube import YouTube
import os
import subprocess

def download_best_quality(url, output_path='.'):
    try:
        yt = YouTube(url)
        
        # Tente de sélectionner d'abord le flux vidéo 1080p à 60fps
        video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True, resolution="1080p", fps=60).first()
        
        if not video_stream:
            # Si 1080p à 60fps n'est pas disponible, essaye avec 1080p à 30fps
            video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True, resolution="1080p").first()
        
        if not video_stream:
            # Si 1080p n'est pas disponible, essaye avec 720p à 60fps
            video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True, resolution="720p", fps=60).first()

        if not video_stream:
            # Si 720p à 60fps n'est pas disponible, essaye avec 720p à 30fps
            video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True, resolution="720p").first()

        if not video_stream:
            print("Aucun flux vidéo trouvé pour les résolutions spécifiées.")
            return

        # Sélectionne le flux audio de la meilleure qualité
        audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()

        if not audio_stream:
            print("Aucun flux audio trouvé.")
            return

        # Télécharge la vidéo et l'audio
        print(f'Téléchargement de la vidéo : {video_stream.resolution} à {video_stream.fps}fps')
        video_file = video_stream.download(output_path=output_path, filename='temp_video.mp4')
        
        print(f'Téléchargement de l\'audio : {audio_stream.abr}')
        audio_file = audio_stream.download(output_path=output_path, filename='temp_audio.mp4')

        # Combinaison de la vidéo et de l'audio en utilisant ffmpeg (assurez-vous d'avoir ffmpeg installé)
        output_file = os.path.join(output_path, yt.title + '.mp4')
        ffmpeg_command = f'ffmpeg -i "{video_file}" -i "{audio_file}" -c copy "{output_file}"'
        print(f'Exécution de la commande ffmpeg : {ffmpeg_command}')
        subprocess.run(ffmpeg_command, shell=True)

        # Supprime les fichiers temporaires
        os.remove(video_file)
        os.remove(audio_file)

        print(f'Vidéo téléchargée et combinée avec succès : {output_file}')
    except Exception as e:
        print(f'Erreur lors du téléchargement : {e}')

if __name__ == "__main__":
    # Exemple d'URL de vidéo YouTube
    url = input("Entrez l'URL de la vidéo YouTube : ")
    output_path = input("Entrez le chemin de sortie (par défaut est le dossier courant) : ")
    if not output_path:
        output_path = '.'
    download_best_quality(url, output_path)

