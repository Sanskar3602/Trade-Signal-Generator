import numpy as np
from orb import observed_trend, ten_thirty, test_total

# Neural network functions using Linear Regression
class NeuralNetwork():

    def __init__(self):
        np.random.seed(1)               # generating random values for our neural network equation
        self.learning_rate = 0.001      # self learning rate
        self.threshold1 = 0.33          # initial vlue for differentiating between downtrend and no trend
        self.threshold2 = 0.66          # initial value for differentiating between uptrend and no trend

    # function for training data
    def train(self, training_inputs, training_outputs, training_iterations):
        for iteration in range(training_iterations):
            output = self.think(training_inputs)
            error = training_outputs - output
            error1 = [0] * len(training_inputs)
            error2 = [0] * len(training_inputs)
            for i in range(len(training_inputs)):
                if(training_outputs[i] == 0):
                    error1[i] = error[i]
                elif(training_outputs[i] == 0.66):
                    error2[i] = error[i]
            sum1 = []
            sum2 = []
            for j in range(len(training_inputs)):
                sum1.append(training_inputs[j]*error1[j])
                sum2.append(training_inputs[j]*error2[j])
            Dth1 = 2/len(training_inputs) * sum(sum1)
            Dth2 = 2/len(training_inputs) * sum(sum2)
            self.threshold1 -= self.learning_rate*Dth1
            self.threshold2 -= self.learning_rate*Dth2

    # function to give output for particular input
    def think(self, inputs):
        inputs = inputs.astype(float)
        output = inputs
        min1 = output.min()
        output -= min1
        max1 = output.max()
        output = output/max1
        for i in range(len(inputs)):
            if(output[i]<self.threshold1):
                output[i] = 0
            elif(output[i] > self.threshold2):
                output[i] = 0.66
            else:
                output[i] = 0.33
        return output

# #---------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    neural_network = NeuralNetwork()

    # Making the values between 0-1

    minima = min(ten_thirty)
    ten_thirty -= minima
    maxima = max(ten_thirty)
    ten_thirty /= maxima

    # Training the data

    neural_network.train(ten_thirty, observed_trend, 1000)
    train_output = neural_network.think(ten_thirty)

    # Calculating Accuracy

    count = 0       # Count to store how many time our output matched actual observed.
    for i in range(len(ten_thirty)):
        if(train_output[i] == observed_trend[i]):
            count += 1
    accuracy = count/len(ten_thirty)
    accuracy *= 100
    print("The Accuracy rate for the Train dataset is: %.2f" %accuracy, "%")


    # Predicting the output based on the test_total value passed from the orb file

    test_total -= minima
    test_total /= maxima
    if(test_total < neural_network.threshold1):
        print("Downtrend Today!")
    elif(test_total > neural_network.threshold2):
        print("Uptrend Today!")
    else:
        print("Can't Say any particular trend")
