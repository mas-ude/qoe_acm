
# Dict for translating itags to quality levels and vice-versa
ITAG_TO_QL = {160: 0,
              133: 1,
              134: 2,
              135: 3,
              136: 4}
QL_TO_ITAG = {v: k for k, v in ITAG_TO_QL.items()}

# Relevant itags
ITAGS = [160, 133, 134, 135]

VIDDEF = {160: {'label': '144p', 'color': 'green', 'resolution':  '256x144'},
          133: {'label': '240p', 'color': 'red'  , 'resolution':  '320x240'},
          134: {'label': '360p', 'color': 'blue' , 'resolution':  '480x360'},
          135: {'label': '480p', 'color': 'grey' , 'resolution':  '640x480'},
          136: {'label': '720p', 'color': 'cyan' , 'resolution': '1280x720'}}

YTPL_LEVELS = {  'tiny': 160,
                'small': 133,
               'medium': 134,
                'large': 135,
                'hd720': 136}

for itag in VIDDEF:
    VIDDEF[itag]['ql'] = ITAG_TO_QL[itag]
    VIDDEF[itag]['itag'] = itag

# YouTube API playback status [1]
PL_STATUS = {-1: 'UNSTARTED',
              0: 'ENDED',
              1: 'PLAYING',
              2: 'PAUSED',
              3: 'BUFFERING',
              5: 'VIDEO_CUED'}
PL_STATUS_STR = {v: k for k, v in PL_STATUS.items()}

# [1] https://developers.google.com/youtube/js_api_reference#Playback_status