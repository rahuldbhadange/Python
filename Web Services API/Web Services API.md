######SOAP: Simple Object Access Protocol





######REST: Representational State Transfer (Architectural style)


representation:
 
    - It is a description of the current state of the resource
    - representation can be XML, JSON. HTML etc.


1. Uniform interface:

    - Resource: Everything is resource
                Any info/data/module can be resource
    
    - URI: any data or resource can be access by URI
           (One to one, one to many, many to many) 
           
           http://xyz.com/employee
           http://xyz.com/employee/{id}
           http://xyz.com/departments
           http://xyz.com/departments/{department}
           http://xyz.com/departments/{department}/{employee}/{id}
    
    - HTTP: GET PUT POST HEADER DELETE 
    
           GET -> http://xyz.com/employee.
                Displayed list of the employee
           GET -> http://xyz.com/employee/{id}
                Displayed details of employee of id={id}
           DELETE -> http://xyz.com/employee/{id}
                Deleted employee of id={id}
           DELETE -> http://xyz.com/departments
                Delete departments
           POST -> http://xyz.com/departments/{department}
                Added new department in departments.
           PUT -> http://xyz.com/departments/{department}/{employee}/{id}
                Updated/modified details of employee of id={id} and in departments={department}

2. Statelessness:  (Stateless)
    - All communication (request/response) between client-server are stateless.
    - The server does not maintain any state (session) of the system, hence client has to send a request which is complete in itself.
    - Client sends a request should be independent and does not depend on any of the previous requests.
    - Because of the server does not have a overhead of maintaining of state/session, it increases performance. 

3. Cacheable: (Caching)
   - It happens at client side
   - Server sends the response of the request that contains header which provides information to client whether server has store request/session or not. 
   - client uses Cache-control header to determine the whether the resource or responds has to be cached or not.
   - This is how client and server coordinate and remains stateless.
  
4. Layered System: (Layering)
    - Multiple layers can exists between client and server.
    - These are http layers. Proxies (evaluating request/simplyfying request)and Gateways (managing the traffic at the server end)
    - Message transfer/translating, improving performance and caching etc.
    - We can also have some layers which can help us in caching.
    - For example: We have layer for caching which stores the response for a hour and if we get request within that hour 
      and there is no change in the resource then we can get back the response from this particular layer and 
      no need to go to the server so it improves performance and scalability.

5. CodeOn Demand (optional):
    - If client request something to server; server responds to the request and the response have the ability to run some code/script.
