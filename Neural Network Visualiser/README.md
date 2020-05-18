<h3>Project on creating neural network visualiser web app.</h3>  
<br>

- Create a model server with Flask and Keras  
- Create a web application with Streamlit  
- Utilize Keras' functional API  

<h4> Some Important points</h4>

- Simple neural network with 2 hidden layers and one output layer and we will visualise the output values from all the nodes in each layer. We will create a simple server with flask to serve the neural network model for inference, and then create simple web app with streamlit and we will use keras functional api to get outputs of hidden layers in addition to the output layer.       
- Here we are not exploring the theory behind the functioning of neural networks.      
- Each box represents a node in a layer and the darker the node image, lower is the output of that node. So completely black would mean 0 and completely white would mean 1.    
- Here we are using the MNIST dataset to train the model.     
- Now, typically we would use ReLU activation for the hidden layers. But here I used sigmoid because we wanted hidden units to have outputs between 0 and 1 for ease of plotting in visualiser app.     
- The model server is created with flask.   
- Now we use Keras functional API to create another model which will have same input as our original model model but it will have output of all the layers except from the input layer.   
- Then, we rearrange the predictions a little bit. When we get a POST request we are gng to return a json object. And since we have a numpy array in the prediction, a json object cannot be created with that data. So we restructure our predictions into a list.  
<br>
<i> In the file ml_server.py I have created a reference to the session that is used for loading the models and then to set it to be used by keras in each request. Models should be loaded only after setting the session so that it works without any error</i>
