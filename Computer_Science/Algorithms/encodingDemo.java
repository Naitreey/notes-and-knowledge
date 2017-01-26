/* 
 * an idiotic encoding and decoding system using bitwise XOR operation
 * */
class encodingdemo {
        public static void main(String[] args) {
                String key="", text="";
                //interpret command-line arguments
                for ( int index=0; index<args.length; index+=2 ) {
                        switch ( args[index] ) {
                                case "-k":
                                        key=args[index+1];
                                        break;
                                case "-t":
                                        text=args[index+1];
                                        break;
                                default:
                                        System.out.println("this weird.");
                                        return;
                        }
                }

                if ( key.equals("") || text.equals("") ) {
                        System.out.println("key (-k) or text (-t) is missing.");
                        return;
                }

                CipherSystem idiotmachine=new CipherSystem(key);
                String orig=text;
                String encoded=idiotmachine.encode(orig);
                System.out.println(encoded);
                System.out.println(idiotmachine.decode(encoded));
        }
}

class CipherSystem {
        String key;
        //constructor
        CipherSystem( String key ) {
                this.key=key;
        }
        //encoding text
        String encode( String orig ) {
                String encoded="";
                char temp;
                for ( int i=0; i<orig.length(); i++ ) {
                        temp=orig.charAt(i);
                        for ( int j=0; j<this.key.length(); j++ ) {
                                temp=(char) (temp ^ this.key.charAt(j));
                        }
                        encoded+=temp;
                }
                return encoded;
        }
        //decode text
        String decode( String encoded ) {
                String orig="";
                char temp;
                for ( int i=0; i<encoded.length(); i++ ) {
                        temp=encoded.charAt(i);
                        for ( int j=this.key.length()-1; j>=0; j-- ) {
                                temp=(char) (temp ^ this.key.charAt(j));
                        }
                        orig+=temp;
                }
                return orig;
        }
}
