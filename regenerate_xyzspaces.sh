here xyz list -p id | tail +3 | head -n -1 | while read ID; do here xyz delete $ID; done

here xyz create -t 'twitter' -d 'twitter sentiment data'
here xyz create -t 'flatzone' -d 'flatzone flat data'

