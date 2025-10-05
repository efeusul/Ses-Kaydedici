import sounddevice as sd #sounddevice ses giriş çıkışını yönetir. kolaylık için sd dedik.
import numpy as np #numpy küçük ses parçalarını tek bir dizide birleştirmeye yarar. kolaylık için np dedik.
import keyboard #keyboad klavye tuş vuruşlarının uygulanması için kullanılır.
import wavio #wavio son NumPy dizisini bir wav. dosyasına yazar. (PCM veri şekli ve örnek genişliği beklenir.)

freq = 44100 #Kaç hz.lik olduğu girilir. Bizim için 44100 iyidir.
channels = 2 # 1-mono , 2-stereo şeklindedir. Kaydedilen dizilerin şeklini belirler.

print("Press 's' to start recording and 'q' to stop.") #Kullanıcının girişi için rehberlik.

recording = [] #Ses parçalarını tutacak bir python listesi.Boş çünkü geldikçe bu listeye eklenecek.
stream = None # sd.InputStream için bir yuvadır. None: kayıt edilmiyor/boş anlamında.


##callback önemli. sounddevice bunu sıklıkla kısa parçalar halinde çağırır.
##indata ses örneklerinin parçasını içeren Numpy dizisi. Şekil: (frames,channels)
##frames parçadaki frame sayısı
##time zamanlama bilgisi.
##status alt ve üst limitleri veya diğer uyarıları gösterir.

def callback(indata, frames, time, status):
    if status:
        print(status) # burada bir uyarı yazması gerekirse yazdır.

    recording.append(indata.copy()) #dıştan içe doğru gidecek olursak: recording.append diyerek
    #mikrofondan gelen ses parçalarını başta oluşturduğumuz boş listeye gönderiyoruz.
    #indata sounddevice kütüphanesi tarafından yeniden kullanılan bir ara bellek olduğundan,
    #copy() ile kalıcı bir kopyası oluşturulur,böylece daha sonra üzerine yazılmaz.
    #hafıza aşımı durumunda recording listesi dolar ve kayıt işlemi sonlanır.
    #hafızaya alınan verileri tek bir çatıda toplamak için de np.concatenate kullanılır.

while True:
    if keyboard.is_pressed("s") and stream is None: #Yalnız kayıt yapmıyorken kullanabilmek için.
        print("Recording... press 'q' to stop.")
        recording = []  # önceki verileri temizler.
        stream = sd.InputStream(samplerate=freq, channels=channels, dtype='int16', callback=callback) #akışı yapılandırmak
        stream.start()

    if keyboard.is_pressed("q") and stream is not None:
        stream.stop()
        stream.close()
        stream = None
        print("Recording stopped.")

        if len(recording) == 0: # Çok hızlı başlatıp bitirirsen kayıt olmadığı için bunu yazdırsın istedik.
            print("No audio recorded, try again!")
        else:
            audio = np.concatenate(recording, axis=0)
            wavio.write("recording.wav", audio, freq, sampwidth=2)
            print("Saved as recording.wav") #kaydı sonlandırdık.
        exit()