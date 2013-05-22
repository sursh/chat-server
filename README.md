## Simple Python chat server with threads and queues.

### What? Why?

At [Hacker School](http://hackerschool.com), I'm exploring concurrency and networking by building a simple chat server a few different ways. The first is the 'dumb' way, using Python's queues and threads data structures. They're not the best tools for the job, but I wanted to see their limitations firsthand before using a more sophisticated tool. 

Next, I'm thinking of adding websockets, then using an event-based framework like Twisted. Then maybe a version in Node.js or Go? Open to suggestions of different ways to approach this sort of networked application. 

### Running it 

1. Set up your virtual environment: `cd .. && virtualenv sockets && cd sockets && source bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
2. `./chat.py` to start your server. Note the port it's listening on (1060 by default).
3. Open a new terminal window for the client. Run `nc localhost 1060`
4. Repeat #4 to start a second chat client and talk to yourself!

### Structure

`main()` sets up a few things: 

- a `masterQueue` of messages waiting to go out to all clients
- `masterSender` daemon to pop messages off `masterQueue'
- a passive socket for client connections

And then it just passively listens for incoming client connections, spinning up a new thread for each one as it goes. 

Each client thread listens for messages from the user and sends them on to the `masterQueue`.

### Known issues

- Python doesn't do real threading. It's all lies. LIES.
- Clients quitting fundamentally breaks things. I tried to try/catch for a while but it's hard to do as the program evolves, since you don't know where it will be when it breaks. It's caused all sorts of error messages as the server evolved, from `broken pipe` to `connection reset by server` and even more mundane Python errors. And sometimes as an added bonus it screws up shared resources so you throw a monkey wrench in other threads too! 
- Clients are not un-registered from the list of activeClients when they quit. Since them quitting breaks everything anyway, I didn't fix this bug. 
- It's hard to see when you're just chatting to yourself, but with real users there's a big UI problem: incoming messages will interfere with your typing. Will fix this with websockets and a real interface.