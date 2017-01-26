package queue;

class QueueEmptyException extends Exception {
        public String toString() {
                return "Queue is empty"
        }
}

class QueueFullException extends Exception {
        int size;

        QueueFullException( int size ) {
                this.size=size;
        }

        public String toString() {
                return "Queue is full, max size is " + this.size;
        }
}

/*
 * fixed-size linear queue implementation
 * */
class FixedLinearQueue implements Queue {
        private int q[];
        private int loc_get, loc_put;

        //initialize cleanly
        FixedLinearQueue(int len) {
                this.q=new int[len];
                loc_get=loc_put=0;
        }
        //initialize from another queue
        FixedLinearQueue( FixedLinearQueue aq ) {
                this.q=new int[aq.size()];
                this.loc_get=aq.loc_get;
                this.loc_put=aq.loc_put;

                for ( int i=0; i<aq.size(); i++ ) {
                        this.q[i]=aq.q[i];
                }
        }
        //initialize using an array
        FixedLinearQueue( int arr[] ) {
                this.q=new int[arr.length];
                this.loc_get=this.loc_put=0;

                for ( int i=0; i<arr.length; i++ ) {
                        this.put( arr[i] );
                }
        }
        //get size of queue
        public int size() {
                return this.q.length;
        }
        //put number in queue
        public void put(int number) {
                try {
                        if ( this.loc_put==q.length ) {
                                throw new QueueFullException( size() );
                        }
                }
                catch ( QueueFullException exobj ) {
                        System.out.println(exobj);
                        return;
                }
                q[this.loc_put++]=number;
        }
        //get number from queue
        public int get() {
                try {
                        if ( this.loc_get==this.loc_put ) {
                                throw new QueueEmptyException();
                        }
                }
                catch ( QueueEmptyException exobj ) {
                        System.out.println(exobj);
                        return -1;
                }
                return q[this.loc_get++];
        }
}

class CircularQueue implements Queue {
        private int q[];
        private int loc_get, loc_put;

        CircularQueue( int len ) {
                this.q=new int[len];
                this.loc_get=this.loc_put=0;
        }
        public void put( int number ) {
                if ( loc_put==q.length ) {
                        loc_put=0;
                }
                q[loc_put++]=number;
        }
}
