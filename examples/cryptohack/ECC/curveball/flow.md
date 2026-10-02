# Flow of the challenge:



#### 'www.bing.com': {"public_key": Point(0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531, 0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A, curve=P256), "curve": "secp256r1","generator": [G.x, G.y]} 
#### G = [0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296, 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5]


## In other to retrieve the packet'www.bing.com' we first look at how the payload works:
### we send:
    * 'private key' $\to$ can't send something like 1,-1 or 0
    * 'host', a random site (i use www.bing.com)
    * 'curve', secp256r1
    * 'generator', a generator key
### The server saves
    * g generator from 'generator'
    * d private key
    * calculate Q = g*d
    * check serach_trusted(Q) to calculate cached, host
### Our point is cached to be 1 to return host
## search_trusted:
### What it does:
    * check if Q == cert['public_key'] $\to$ return true, host
### Mindset:
#### we need host to be "www.bing.com" to bring out the flag.
 #### so we need Q == "www.bing.com" ['public_key']
 #### We have its public_key, we can send generator and d publickey
 #### which is enough since we can manipulate generator*d = public_key
 #### since u can send anything, we can choose d =2 to easily calculate (we can send anything but it's not recommended to choose anything further than > 100 since n mod is very big).
 #### We have n mod of P256 $\to$  0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
 #### We can do: generator = public_key* (d^-1 mod n)
 #### Therefore we can get the flag! 







