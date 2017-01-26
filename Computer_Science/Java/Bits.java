class Bits {
        int bitnum;
        //constructor
        Bits( int num ) {
                this.bitnum=num;
        }
        //show lowest `bitnum' bits of `number'
        void showbits(int number) {
                for ( int mask=1<<(this.bitnum-1); mask!=0; mask>>>=1 ) {
                        if ( (number & mask)!=0 ) {
                                System.out.print("1");
                        }
                        else {
                                System.out.print("0");
                        }
                }
                System.out.println();
        }
}
