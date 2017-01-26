class stackdemo {
        public static void main(String[] args) {
                Stack s1=new Stack( 10 );
                for ( int i=0; i<s1.size; i++ ) {
                        s1.put(i);
                }
                Stack s2=new Stack( s1 );
                int ar[]={ 10,9,2,3,4,5,32,4,2,4,5,6,3,3 };
                Stack s3=new Stack( 20, ar );

                for ( int i=0; i<s1.size; i++ ) {
                        System.out.print(s1.get() + " ");
                }
                System.out.println();
                for ( int i=0; i<s2.size; i++ ) {
                        System.out.print(s2.get() + " ");
                }
                System.out.println();
                for ( int i=0; i<s3.size; i++ ) {
                        int result=s3.get();
                        if ( result!=-999 ) {
                                System.out.print(result + " ");
                        }
                        else {
                                break;
                        }
                }
                System.out.println();
        }
}

class Stack {
        private int data[];
        public int size;
        private int loc_put, loc_get;
        //constructors
        Stack( int size ) {
                this.data=new int[size];
                this.size=size;
                this.loc_put=0;
                this.loc_get=-1;
        }
        Stack( int size, int ar[] ) {
                this.data=new int[size];
                this.size=size;
                this.loc_put=0;
                this.loc_get=-1;
                for ( int i=0; i<ar.length; i++ ) {
                        this.put(ar[i]);
                }
        }
        Stack( Stack s ) {
                this.data=new int[s.size];
                this.size=s.size;
                this.loc_put=0;
                this.loc_get=-1;
                for ( int i=0; i<this.size; i++ ) {
                        this.put(s.data[i]);
                }
        }
        //put & get methods
        public void put( int number ) {
                if ( this.loc_put<this.data.length ) {
                        this.data[this.loc_put]=number;
                        this.loc_get++;
                        this.loc_put++;
                }
                else {
                        System.out.println("full");
                }
        }
        public int get() {
                if ( this.loc_get>=0 ) {
                        this.loc_put--;
                        return this.data[this.loc_get--];
                }
                else {
                        System.out.println("empty");
                        return -999;
                }
        }
}
