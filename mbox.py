import RPi.GPIO as GPIO
import MFRC522
import signal
import ndef
from time import sleep
import spotify
import threading

# marks last tlv block in data area
CACHE_SIZE_IN_MB = 1024
TERMINATOR_TLV = b'\xFE'
continue_reading = True
URI_RECORD_TYPE = 'urn:nfc:wkt:U'

logged_in_event = threading.Event()


def connection_state_listener(signal_session):
    if signal_session.connection.state is spotify.ConnectionState.LOGGED_IN:
        logged_in_event.set()


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    session.player.pause()
    session.player.unload()
    GPIO.cleanup()


def playing_on_other_device(signal_session):
    print("pausing due to PLAY_TOKEN_LOST")
    signal_session.player.pause()


def on_song_end(signal_session):
    play_next_song()


def play_next_song():
    print('playing next song')
    print('songs in queue:')
    print(tracks)
    global tracks
    if tracks:
        track = tracks.pop(0)
        track.load()
        session.player.load(track)
        session.player.play()
        global playing
        playing = True


print('logging in...')
config = spotify.Config()
config.cache_location = b'/home/pi/cache'
config.user_agent = 'mbox'
session = spotify.Session(config=config)
session.set_cache_size(CACHE_SIZE_IN_MB)
session.on(
    spotify.SessionEvent.CONNECTION_STATE_UPDATED,
    connection_state_listener)
# session.login('username', 'password', remember_me=True)
tracks = []
session.relogin()
session.on(spotify.SessionEvent.PLAY_TOKEN_LOST, playing_on_other_device)
session.on(spotify.SessionEvent.END_OF_TRACK, on_song_end)
event_loop = spotify.EventLoop(session)
event_loop.start()
while not logged_in_event.wait(0.1):
    session.process_events()
print('logged in')

print('obtaining audio sink...')
audio_driver = spotify.AlsaSink(session)
print('Ready to play')
playing = False
num_of_cycles_card_not_found = 0

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
MIFAREReader = MFRC522.MFRC522()
while continue_reading:
    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status != MIFAREReader.MI_OK and playing:
        num_of_cycles_card_not_found = num_of_cycles_card_not_found + 1
        if num_of_cycles_card_not_found >= 2:
            print('card removed while playing, pausing playback')
            session.player.pause()
            playing = False

    # If a card is found
    if status == MIFAREReader.MI_OK and playing:
        num_of_cycles_card_not_found = 0
    if status == MIFAREReader.MI_OK and not playing:
        print("Card detected")
        (status, uid) = MIFAREReader.MFRC522_SelectTagSN()
        if status == MIFAREReader.MI_OK and not playing:
            # Select the scanned tag
            # MIFAREReader.MFRC522_SelectTag(uid)
            num_of_cycles_card_not_found = 0
            i = 0
            result = []
            while True:
                temp_data = MIFAREReader.MFRC522_Read(i)
                if temp_data is None:
                    break
                result = result + temp_data[:4]
                # print(bytes(temp_data).decode("ascii","ignore"))
                # print("\n")
                i = i + 1
                if TERMINATOR_TLV in temp_data:
                    break
            # MIFAREReader.MFRC522_StopCrypto1()
            for record in ndef.message_decoder(bytes(result[23:])):
                if record.type == URI_RECORD_TYPE:
                    print('loading album ' + record.iri)
                    album = session.get_album(record.iri)
                    # not sure if we need it
                    # album.load()
                    album_browser = album.browse()
                    album_browser.load()
                    tracks_sequence = album_browser.tracks
                    for t in tracks_sequence:
                        tracks.append(t)
                    play_next_song()
                    break
    MIFAREReader.MFRC522_StopCrypto1()
    sleep(1)
