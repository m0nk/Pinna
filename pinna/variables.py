class settings:
  stop_on_exit='0'
  alarm_hour='00'
  alarm_minute='00'
  alarm_enable='0'
  alarm_volume='0'
  mpd_host='127.0.0.1'
  mpd_port='6600'
  mpd_pass= ''
  music_directory= ''

class checks:
  song=-1
  shuffle='0'
  repeat='0'
  last_song=None
  playlist_version=0

class main_vars:
  shuffle_id=None
  repeat_id=None
  album_art='1'
  main_window=1

class info_vars:
  view='lyrics'
  
class browser_vars:
  view=None
  browser_list=[None,[]]
  playlist_list=[None,[]]
  current_playlist=[None,[]]

