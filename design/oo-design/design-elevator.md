# Design Ele‍‌‍‌‍‍‍‌‍‍‌‍‌‌‍‌vator:
- First ask the interviewer what kind of elevator?  there is only one elevator serving that building or multiple elevators serving the building simultaneously?

- In this problem, thesituation is that: there is one elevator serving the building.  there are many floors in the buliding. Maybe there are some users in different floor pressing the button simultaneously. This results in some requests to RequestProcessCenter for processing. The  RequestProcessCenter figure out the first request that need to be processed in such an algorithm that the distance between target floor and current floor is shortest.

- Describe the whole situation first and check it with your interviewer then sketch out the main classes and methods on the whiteboard;

So we need the following classes:
### User
```java
public class User {
    private name;
    public pressButton(int toFloor) {
        Request r‍‌‍‌‍‍‍‌‍‍‌‍‌‌‍‌eq = new Request( toFloor);
        RequestProcessCenter  center = RequestProcessCenter.getInstance();
        center.addRequest(req);
    }
}
```

---
### Request
```java
public class Request {
    private int toFloor;
    public Request(int _toFloor) {
        toFloor = _toFloor;
    }   

    public getToFloor() {
        return toFloor;
    }
}

```

---


### Elevator
```java
public class Elevator {
    public static Elevator instance = null;
    private int currentFloor;

    public static Elevator( ) {
        if (instance == null) {  
        // late loading and eager loading
        // connection pool
            synchronized (Elevator.class) {
                instance = new Elevator();
            }
        }
        return instance;
    }
    public getInstance() {
        if (instance == null) {
            synchronized (SingletonDemo.class) {
                if (instance == null) { // Check again
                    instance = new Elevator();
            }   
        }
        return instance;
    }

    public getCurrentFloor() {
        return currentFloor;
    }

    public moveToTargetFloor(int toFloor) {
        currentFloor = toFloor;
    }
    public void moveUp();
    public void moveDown();
}
```

---

### RequestProcessCenter

```java
public RequestProcessCenter implements runnable {
    public LinkedList<Request> queue;

    public RequestProcessCenter( ) {
        queue = new LinkedList<Request>( );
    }
    public void run() {
        while ( true ) {
            processRequest( )
        }
    }
    public void addRequest(Request request) {
        queue.add(request);
    }

    public void removeRequest(Request request) {
        queue.remove(request);
    }
    public Request getNextRequest( ) {
        Request shortestReq = null;
        int shortest = Integer.MAX_VALUE;
        int curFloor = Elevator.getInstance( ).getCurrentFloor( );
        for (Request item : queue) {
            int distance = Math.abs(curFloor - item.getToFloor( ) );
            if (distance < shortest) {
                shortest = distance;
                shortestReq = item;
            }       
        }
        return shortestReq;
    }

    public void processRequest( ) {
        Request req = getNextRequest( );
        if (req != null) {
            int toFloor = req.getToFloor( );
            Elevator.getInstance.moveToTargetFloor( toFloor);
            queue.remove(req);
        }
       
    }
}
```

