#/bin/zsh
                                                                                                    
MON="eDP-1"    # Discover monitor name with: xrandr | grep " connected"                             
STEP=0.05      # Step Up/Down brightnes by
                                                                                                    
# get current brightness                                                                            
CurrBrightness="$(xrandr --verbose | awk '/Brightness/ {print $2;exit}')"

# if we are above 1.0 the minimal possible step is 0.1
if [[ $CurrBrightness -gt 1.0 ]]
then
  STEP=0.1
fi
# check whether increase or decrease brightness                                                     
if [ $1 = "+" ] 
then 
  NewBrightness=$((CurrBrightness + STEP))
elif [ $1 = "-" ]
then
  NewBrightness=$(( CurrBrightness - STEP ))
else
  echo 'specify + or - as argument'
  exit 1
fi
                                                                                                    

# blackscreen not wanted -> min brightness is 0.05                                                  
if [[ "$NewBrightness" -lt 0.05 ]]
then
  NewBrightness=0.05
# too bright display not wanted -> max brightness is 1
# changed to max of 1.2 (in case I sit outside in the sun)
elif [[ "$NewBrightness" -gt 1.2 ]]
then                                                                 
  NewBrightness=1.20
fi                                                                                                  
echo $NewBrightness
# change to new brightness                                                                          
xrandr --output "$MON" --brightness "$NewBrightness"
