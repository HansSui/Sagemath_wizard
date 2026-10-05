# Flow of this challenge
## What we can find:
    * Challenge called for input everything with "options"
        * 'sign_time' $\to$ return signature of the function sign_time
        * 'verify' $\to$ gives us payloads to give:
            * 'msg', 'r', 's'
            And then verify, if it's true:
                * if messenger == 'unlock':
                    * $\to$ flag
## Each function
### sign_time:
    * check the datetime now:
    * m = minute
    * n = second
    * msg = "Current time is m:n"
    * h =sha1(msg)
    * sig = using privkey to sign using(h, random 1--> n) 
    * return sign_time, hex(sig.r), hex(sig.s)
### Verify:
    * check verify the sign_time
    * Using verifies(hsh,sig) to check hsh 
    * hsh: bytes_to_log(sha1(msg))  
    * sig_r, sig_s
    * sig = Signature(sig_r, sig_s) and then check if sig == hsh --> return true
### The data: 
#### using d in the range of (1,n) where n is 6277101735386680763835789423176059013767194773182842284081
#### Public_key(g, g* d) $\to$ it generates Pub = g*d
#### since d coulbe be very big num so we can snap out options: discreet_log.
#### We need the message to be 'unlock'
    * Same public_key, different msg 
    * Has to be the same sig for 'unlock'
    * So if i can call sign_time and input the current? $\to$ prob not
    * But i do notice that this one i can see that they reuse hsh key so what happened if i can spam sending the same payload? since they also use sha1 to sign --> might be HNP