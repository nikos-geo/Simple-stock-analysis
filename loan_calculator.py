import os
import requests
from tkinter import *
from tkinter import messagebox


class LoanCalculator:
      def __init__(self):

        # Create a window
        window = Tk()
        window.title("Loan Calculator") # Set title

        # Create the input boxes
        Label(window, text = "Annual Interest Rate").grid(row=1,
                                                        column=1, sticky=W)
        Label(window, text="Number of years").grid(row=2,
                                                   column=1, sticky=W)
        Label(window, text="Loan amount (Face Value or Principal)").grid(row=3,
                                                                         column=1, sticky=W)
        Label(window, text="Monthly payment").grid(row=4, 
                                                   column=1, sticky=W)
        Label(window, text="Total amount paid (Principal + Interest)").grid(row=5,
                                                                            column=1, sticky=W)
        # Taking inputs
        self.annualInterestRateVar = StringVar()
        Entry(window, textvariable= self.annualInterestRateVar,
              justify= RIGHT).grid(row=1, column=2)

        self.numberOfYearsVar = StringVar()
        Entry(window, textvariable= self.numberOfYearsVar,
              justify= RIGHT).grid(row=2,column=2)

        self.faceValue = StringVar()
        Entry(window, textvariable= self.faceValue,
              justify=RIGHT).grid(row=3, column=2)

        self.monthlyPmtVar = StringVar()
        lblMonthlyPmt = Label(window, textvariable= 
                              self.monthlyPmtVar).grid(row=4,column=2, sticky=E)

        self.totalAmountVar = StringVar()
        lblTotalAmount = Label(window, textvariable= 
                               self.totalAmountVar).grid(row=5, column=2, sticky=E)
        # create the button 
        btComputePayment= Button(window, text= "Compute payment",
                                 command= self.computePayment).grid(
                                     row=6, column=2, sticky=E)
                                 
        window.mainloop()

      def computePayment(self):
          monthlyPayment = self.getMonthlyPayment(float(self.faceValue.get()),
                                                  float(self.annualInterestRateVar.get()) / 1200,
                                                  int(self.numberOfYearsVar.get()))
          self.monthlyPmtVar.set(format(monthlyPayment, '10.2f'))
          totalPayment = float(self.monthlyPmtVar.get()) * 12 \
                                                      * int(self.numberOfYearsVar.get())
          self.totalAmountVar.set(format(totalPayment, '10.2f'))

      def getMonthlyPayment(self, faceValue, monthlyInterestRate, numberOfYears):
          monthlyPayment = faceValue * monthlyInterestRate / (1- 1 / (1 + monthlyInterestRate) ** (numberOfYears * 12))
          return monthlyPayment
          
             
LoanCalculator()