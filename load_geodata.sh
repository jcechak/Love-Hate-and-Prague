TWITTER_LAYER_ID=`here xyz list | grep 'twitter' | cut -f 1 -d ' '`
here xyz clear $TWITTER_LAYER_ID
here xyz upload $TWITTER_LAYER_ID -f twitter_geodata.json

FLATZONE_LAYER_ID=`here xyz list | grep 'flatzone' | cut -f 1 -d ' '`
here xyz clear $FLATZONE_LAYER_ID
here xyz upload $FLATZONE_LAYER_ID -f flatzone_geodata.json

