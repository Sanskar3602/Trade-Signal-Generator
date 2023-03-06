import numpy as np
from orb import observed_trend, ten_thirty, test_total

# Neural network functions using Linear Regression
class NeuralNetwork():

    def __init__(self):
        np.random.seed(1)               # generating random values for our neural network equation
        self.learning_rate = 0.001      # self learning rate
        self.threshold1 = 0.33          # initial threshold for differentiating between downtrend and no trend
        self.threshold2 = 0.66          # initial threshold for differentiating between uptrend and no trend

    # function for training data
    def train(self, training_inputs, training_outputs, training_iterations):
        for iteration in range(training_iterations):
            output = self.think(training_inputs)
            error = training_outputs - output
            error1 = [0] * len(training_inputs)
            error2 = [0] * len(training_inputs)
            for i in range(len(training_inputs)):
                if(training_outputs[i] == 0):
                    error1[i] = training_inputs[i] * error[i]
                elif(training_outputs[i] == 0.66):
                    error2[i] = training_inputs[i] * error[i]
            delta1 = 2/len(training_inputs) * sum(error1)
            delta2 = 2/len(training_inputs) * sum(error2)
            self.threshold1 -= self.learning_rate * delta1
            self.threshold2 -= self.learning_rate * delta2

    # function to give output for particular input
    def think(self, inputs):
        output = inputs.astype(float)       # Converting to float for more precision

        # Adjusting the value of output between 0-1
        
        minimum_output = output.min()
        output -= minimum_output
        max_value = output.max()
        output = output/max_value

        for i in range(len(inputs)):
            if(output[i]<self.threshold1):
                output[i] = 0
            elif(output[i] > self.threshold2):
                output[i] = 0.66
            else:
                output[i] = 0.33
        return output

# ---------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    neural_network = NeuralNetwork()        # Initializing the Neural Network

    # Scaling the values between 0-1

    minima = min(ten_thirty)
    ten_thirty -= minima
    maxima = max(ten_thirty)
    ten_thirty /= maxima

    # Training the data

    neural_network.train(ten_thirty, observed_trend, 1000)      # Iterating 1000 times for training data
    train_output = neural_network.think(ten_thirty)             # Training our input

    # Calculating Accuracy

    count_correct_prediction = 0       # To store how many times, our output matched actual observed.
    for i in range(len(ten_thirty)):
        if(train_output[i] == observed_trend[i]):
            count_correct_prediction += 1
    accuracy = count_correct_prediction/len(ten_thirty)         # Calculating accuracy
    accuracy *= 100
    print("The Accuracy rate over the Train dataset is: %.2f" %accuracy, "%")

    # Converting the test value based on previous values of minima and maxima

    test_total -= minima
    test_total /= maxima

    # Predicting the output based on the test_total value passed from the orb file

    if(test_total < neural_network.threshold1):
        print("Downtrend Today!")
    elif(test_total > neural_network.threshold2):
        print("Uptrend Today!")
    else:
        print("Can't Say any particular trend")
