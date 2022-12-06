import numpy as np
import matplotlib.pyplot as plt
from orbreqd import ans, tenthirty, total

class NeuralNetwork():

    def __init__(self):
        np.random.seed(1)
        self.learning_rate = 0.001
        self.threshold1 = 0.33
        self.threshold2 = 0.66

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

    minima = min(tenthirty)
    tenthirty -= minima
    maxima = max(tenthirty)
    tenthirty /= maxima
    neural_network.train(tenthirty, ans, 1000)
    train = neural_network.think(tenthirty)
    count = 0
    count1 = 0
    for i in range(len(tenthirty)):
        if(train[i] == ans[i]):
            count += 1
    total -= minima
    total /= maxima
    # print(total)
    accuracy = count/len(tenthirty)
    print(accuracy)
    if(total < neural_network.threshold1):
        print("down")
    elif(total>neural_network.threshold2):
        print("up")
    else:
        print("none")
