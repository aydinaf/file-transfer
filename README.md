To run:
Install Python on your device and start server.py. Enter 0.0.0.0 for IP, and a high port number (ex: 15000). 
Then run client.py and enter an IP address (ex: the local IP address of your device) and the same port number entered for server.py.
On client enter a command such as put test.txt or other available commands. help command will return a list of available commands.
========================================
<h1># file-transfer</h1>
<h2>A pair of client and server Python programs that facilitate transfer of files between the two hosts.</h2>
<p>This project contains a pair of client-server programs that communicate via Python stream sockets and simulate partially the<br />file transfer protocol (FTP). The main purpose of these client/server programs is to give the client the ability to<br />download files from the server directory to the client directory and upload files of any type from the client directory to the<br />server directory.</p>
<h3>Client User Commands:</h3>
<blockquote>
<ul>
<li>
<h4>put fileName</h4>
</li>
<li>
<h4>get fileName</h4>
</li>
<li>
<h4>change oldFileName newFileName</h4>
</li>
<li>
<h4>help</h4>
</li>
<li>
<h4>bye</h4>
</li>
</ul>
</blockquote>
