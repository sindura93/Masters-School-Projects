
import sys

if sys.version_info[0] < 3:
	import Tkinter as tk
else:
	import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.backends.tkagg as tkagg
import random
import os
import pandas as pd
import operator
import scipy.misc
from sklearn.metrics import confusion_matrix
from keras import initializers 
from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers
from keras.metrics import mean_squared_error, mean_absolute_error
import keras.backend as K
from sklearn.cross_validation import train_test_split

class MainWindow(tk.Tk):
    
    def __init__(self, debug_print_flag=False):
        tk.Tk.__init__(self)
        self.debug_print_flag = debug_print_flag
        self.master_frame = tk.Frame(self)
        self.master_frame.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.rowconfigure(0, weight=1, minsize=500)
        self.columnconfigure(0, weight=1, minsize=500)
        # set the properties of the row and columns in the master frame
        self.master_frame.rowconfigure(2, weight=10, minsize=400, uniform='xx')
        self.master_frame.columnconfigure(0, weight=1, minsize=200, uniform='xx')
        # create all the widgets
        self.left_frame = tk.Frame(self.master_frame)
        # Arrange the widgets
        self.left_frame.grid(row=2, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        # Create an object for plotting graphs in the left frame
        self.display_mse = LeftFrame(self, self.left_frame, debug_print_flag=self.debug_print_flag)
        

class LeftFrame:

    def __init__(self, root, master, debug_print_flag=False):
        self.master = master
        self.root = root
        #########################################################################
        #  Set up the constants and default values
        #########################################################################
        self.xmin = 0
        self.xmax = 1000
        self.ymin = -100000
        self.ymax = 100000
        self.file_path = "stock_data.csv" #"data_set_2.csv"
        self.delayedElements_val = 10
        self.alpha_val = 0.1
        self.trainingSampleSize_val = 80
        self.stride_val = 1
        self.numIterations_val = 10
        self.bias_vec = 0
        self.weight_vec = np.array([])
        self.normalized_data = self.normalize_data()
        self.data_samples, self.targets = self.make_samples_targets()        
        self.mse_arr = np.array([])
        self.mae_arr = np.array([])        
        #########################################################################
        #  Set up the plotting frame and controls frame
        #########################################################################
        master.rowconfigure(0, weight=10, minsize=400)
        master.columnconfigure(0, weight=10)
        self.plot_frame = tk.Frame(self.master, borderwidth=10, relief=tk.SUNKEN)
        self.plot_frame.grid(row=0, column=0, columnspan=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self.figure = plt.figure(figsize=(10,10))
        self.axes1 = self.figure.add_subplot(121)
        self.axes1.set_xlabel('Epochs')
        self.axes1.set_ylabel('Mean Squared Error')
        self.axes1.set_title("")
        self.axes2 = self.figure.add_subplot(122)
        self.axes2.set_xlabel('Epochs')
        self.axes2.set_ylabel('Max Absolute Error')
        self.axes2.set_title("")
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        # Create a frame to contain all the controls such as sliders, buttons, ...
        self.controls_frame = tk.Frame(self.master)
        self.controls_frame.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        #########################################################################
        #  Set up the control widgets such as sliders and selection boxes
        #########################################################################
        self.delayedElements_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                               from_=0, to_=100, resolution=1, bg="#DDDDDD", activebackground="#FF0000",
                                               highlightcolor="#00FFFF", label="Number of Delayed Elements",
                                               command=lambda event: self.delayedElements_slider_callback())
        self.delayedElements_slider.set(self.delayedElements_val)
        self.delayedElements_slider.bind("<ButtonRelease-1>", lambda event: self.delayedElements_slider_callback())
        self.delayedElements_slider.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        
        self.alpha_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                            from_=-0.001, to_=1.0, resolution=0.01, bg="#DDDDDD",
                                            activebackground="#FF0000", highlightcolor="#00FFFF", 
                                            label="Alpha (learning rate)",
                                            command=lambda event: self.alpha_slider_callback())
        self.alpha_slider.set(self.alpha_val)
        self.alpha_slider.bind("<ButtonRelease-1>", lambda event: self.alpha_slider_callback())
        self.alpha_slider.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        
        self.trainingSampleSize_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                              from_=0, to_=100, resolution=1, bg="#DDDDDD", activebackground="#FF0000",
                                              highlightcolor="#00FFFF", label="Training Sample Size (Percentage)",
                                              command=lambda event: self.trainingSampleSize_slider_callback())
        self.trainingSampleSize_slider.set(self.trainingSampleSize_val)
        self.trainingSampleSize_slider.bind("<ButtonRelease-1>", lambda event: self.trainingSampleSize_slider_callback())
        self.trainingSampleSize_slider.grid(row=0, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
        
        self.stride_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL, from_=0,
                                      to_=100, resolution=1, bg="#DDDDDD", activebackground="#FF0000",
                                      highlightcolor="#00FFFF", label="Stride", 
                                      command=lambda event: self.stride_slider_callback())
        self.stride_slider.set(self.stride_val)
        self.stride_slider.bind("<ButtonRelease-1>", lambda event: self.stride_slider_callback())
        self.stride_slider.grid(row=1, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
        
        self.numIterations_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL, from_=0,
                                             to_=100, resolution=1, bg="#DDDDDD", activebackground="#FF0000",
                                             highlightcolor="#00FFFF", label="Number of Iterations",
                                             command=lambda event: self.numIterations_slider_callback())
        self.numIterations_slider.set(self.numIterations_val)
        self.numIterations_slider.bind("<ButtonRelease-1>", lambda event: self.numIterations_slider_callback())
        self.numIterations_slider.grid(row=0, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
        
        #########################################################################
        #  Set up the buttons
        #########################################################################
        self.initialize_weights_btn = tk.Button(self.controls_frame, text="Set Weights to Zero", 
                                                command=self.initialize_weights)
        self.initialize_weights_btn.grid(row=1, column=2)
        self.adjust_weights_lms_btn = tk.Button(self.controls_frame, text="Adjust Weights (LMS)", 
                                            command=self.adjust_weights_lms)
        self.adjust_weights_lms_btn.grid(row=0, column=3)
        self.adjust_weights_direct_btn = tk.Button(self.controls_frame, text="Adjust Weights (Direct)",
                                                   command=self.adjust_weights_direct)
        self.adjust_weights_direct_btn.grid(row=1, column=3)
        self.canvas.get_tk_widget().pack(side="top",fill="both",expand=True)
         
    def alpha_slider_callback(self):
        self.alpha_val = np.float(self.alpha_slider.get())
    
    def delayedElements_slider_callback(self):
        self.delayedElements_val = self.delayedElements_slider.get()
    
    def trainingSampleSize_slider_callback(self):
        self.trainingSampleSize_val = self.trainingSampleSize_slider.get()
    
    def stride_slider_callback(self):
        self.stride_val = self.stride_slider.get()
    
    def numIterations_slider_callback(self):
        self.numIterations_val = self.numIterations_slider.get()
        
    def normalize_data(self):
        data = pd.read_csv(self.file_path)
        normalized_data = pd.DataFrame()
        normalized_data['Price Change'] = (2*((data.iloc[:,0]-min(data.iloc[:,0]))/(max(data.iloc[:,0])-min(data.iloc[:,0]))))-1
        normalized_data['Volume Change'] = (2*((data.iloc[:,1]-min(data.iloc[:,1]))/(max(data.iloc[:,1])-min(data.iloc[:,1]))))-1
        return normalized_data
    
    def make_samples_targets(self):
        initial_data = self.normalized_data
        price_arr = np.array(np.transpose(initial_data['Price Change']))
        volume_arr = np.array(np.transpose(initial_data['Volume Change']))
        data_samples = np.array([])
        targets = np.array([])
        if len(initial_data) > self.delayedElements_val:
            #pull inputs and targets together
            price_X, price_Y = self.get_input_target(price_arr)
            targets = price_Y
            volume_X, volume_Y = self.get_input_target(volume_arr)
            data_samples = np.concatenate((price_X, volume_X), axis=1)
        print("\n data samples shape: \n", data_samples.shape)
        print("\n targets shape: \n", targets.shape)
        return data_samples, targets
                
    def get_input_target(self, inputColumn_arr):
        col_X = inputColumn_arr
        columnSamples_X = np.array([])
        inputColumn_Y = np.array([])
        delay_range = self.delayedElements_val+1
        stride = self.stride_val
        while(len(col_X) >= delay_range+1):            
            temp_X = np.delete(col_X, np.s_[delay_range+1:])
            col_Y = np.delete(col_X, np.s_[:-1])
            temp_X = np.delete(temp_X, np.s_[-1:])
            col_X = np.delete(col_X, np.s_[:stride])
            columnSamples_X = np.append(columnSamples_X, temp_X)
            columnSamples_X = columnSamples_X.reshape(int(len(columnSamples_X)/delay_range), delay_range)
            inputColumn_Y = np.append(inputColumn_Y, col_Y)
        return columnSamples_X, inputColumn_Y
    
    def initialize_weights(self):
        print("button1")
        self.weight_vec=np.array([])
        self.bias_vec=0
        
    def adjust_weights_lms(self):
        self.weight_vec=np.array([])
        self.bias_vec=0
        self.mse_arr = np.array([])
        self.mae_arr = np.array([])
        self.normalized_data = self.normalize_data()
        self.data_samples, self.targets = self.make_samples_targets()
        neuron_lms_seqmodel = Sequential()
        neuron_lms_seqmodel.add(Dense(units=1, input_dim=2*(self.delayedElements_val+1), kernel_initializer=initializers.Zeros()))
        error_optimizer = optimizers.SGD(lr=2*self.alpha_val)
        neuron_lms_seqmodel.compile(loss='mse', optimizer=error_optimizer, metrics=[mean_squared_error, max_absolute_err])
        validation_splitval = round((1 - (self.trainingSampleSize_val/100)),2)
        scores = neuron_lms_seqmodel.fit(self.data_samples, self.targets, batch_size=32, epochs=self.numIterations_val, validation_split=validation_splitval)
        self.weight_vec = neuron_lms_seqmodel.layers[0].get_weights()[0]
        self.bias_vec = neuron_lms_seqmodel.layers[0].get_weights()[1][0]
        self.mse_arr = scores.history['val_mean_squared_error']
        self.mae_arr = scores.history['val_max_absolute_err']
        self.plot_error()
        
    def adjust_weights_direct(self):
        self.weight_vec=np.array([])
        self.bias_vec=0
        self.mse_arr = np.array([])
        self.mae_arr = np.array([])
        self.normalized_data = self.normalize_data()
        self.data_samples, self.targets = self.make_samples_targets()
        X_train, X_test, y_train, y_test = train_test_split(self.data_samples, self.targets, train_size=0.8)
        z_mat = self.calculate_Z_mat(X_train)
        h_mat = self.calculate_h_mat(z_mat, y_train)
        R_inv_mat = self.calculate_R_inv_mat(np.transpose(z_mat))
        #calculate and freeze weights
        weight_vec = np.dot(R_inv_mat, h_mat)
        self.weight_vec = weight_vec[0:22]
        self.bias_vec = weight_vec[22]
        #calculate metrics for test data
        z_mat_test = self.calculate_Z_mat(X_test)
        #h_mat_test = self.calculate_h_mat(z_mat_test, y_test)
        y_pred = np.dot(np.transpose(weight_vec),np.transpose(z_mat_test))
        error_mat = y_test - y_pred
        for i in range(self.numIterations_val):
            #error_mat_sum = 0.0
            #error_mat_max = 0.0
            error_mat_square = 0.0
            for j in range(len(error_mat)):
                #error_mat_sum += np.abs(error_mat[j])
                error_mat_square += (np.abs(error_mat[j]))**2
            #mae_value = (error_mat_sum/len(error_mat))
            mae_value = np.max(np.abs(error_mat))
            mse_value = (error_mat_square/len(error_mat))
            self.mae_arr = np.append(self.mae_arr, mae_value)
            self.mse_arr = np.append(self.mse_arr, mse_value)
        self.plot_error()
    
    def calculate_Z_mat(self, train_x):
        newshape = train_x.shape[1] + 1
        new_input_mat = np.array([])
        for index, val in enumerate(train_x):
            input_bias_row = np.append(val, 1)
            new_input_mat = np.append(new_input_mat, input_bias_row)
        new_input_mat = new_input_mat.reshape(int(len(new_input_mat)/newshape), newshape)
        #new_input_mat = np.transpose(new_input_mat)
        return new_input_mat
        
    def calculate_h_mat(self, z_mat, train_y):
        sample_h = np.array([])
        for index, val in enumerate(z_mat):
            if(len(sample_h) == 0):
                sample_h = (train_y[index] * val) / len(train_y)
            else:
                sample_h = sample_h + (train_y[index] * val) / len(train_y)
        return sample_h        
        
    def calculate_R_inv_mat(self, z_mat):
        R_mat = (np.dot(z_mat, np.transpose(z_mat)))/len(z_mat)
        R_mat_inv = np.linalg.inv(R_mat)
        return R_mat_inv
    
    def plot_error(self):
        self.axes1.cla()
        self.axes2.cla()
        self.axes1.set_xlabel('Epochs')
        self.axes1.set_ylabel('Mean Squared Error')
        self.axes2.set_xlabel('Epochs')
        self.axes2.set_ylabel('Max Absolute Error')
        plotMSEdata = self.mse_arr
        plotMAEdata = self.mae_arr
        mse_x_axis = [i for i in range(len(plotMSEdata))]
        mae_x_axis = [i for i in range(len(plotMAEdata))]
        self.axes1.plot(mse_x_axis, plotMSEdata, c= 'purple')
        self.axes2.plot(mae_x_axis, plotMAEdata, c= 'magenta')
        self.canvas.draw()
        
def close_window_callback(root):
    if tk.messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()
        
def max_absolute_err(y_true,y_pred):
    return K.max(K.abs(y_true - y_pred), axis = -1)

main_window = MainWindow(debug_print_flag=False)
main_window.wm_state('zoomed')
main_window.title('Stock Price Prediction using Adaline Filter')
main_window.minsize(800, 600)
main_window.protocol("WM_DELETE_WINDOW", lambda root_window=main_window: close_window_callback(root_window))
main_window.mainloop()
