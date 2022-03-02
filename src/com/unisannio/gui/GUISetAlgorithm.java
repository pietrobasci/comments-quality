package com.unisannio.gui;

import java.awt.BorderLayout;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.JComboBox;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JTextField;

import com.unisannio.controller.AnalysisControl;

import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.StringTokenizer;
import java.util.Vector;


public class GUISetAlgorithm extends JFrame {

	private static final long serialVersionUID = 1L;
	private JPanel contentPane;
	private JTextField textField;

	/**
	 * Create the frame.
	 */
	public GUISetAlgorithm(AnalysisControl control) {

		setTitle("Algorithm");
		setBounds(200, 200, 450, 300);
		setResizable(false);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(25, 25, 25, 25));
		contentPane.setLayout(new BorderLayout(0, 0));
		setContentPane(contentPane);
		
		JPanel panel = new JPanel();
		panel.setBorder(new EmptyBorder(20, 0, 0, 0));
		contentPane.add(panel, BorderLayout.CENTER);
		panel.setLayout(new FlowLayout(FlowLayout.CENTER, 5, 5));
		
		JLabel lblNewLabel = new JLabel("Classifier options: ");
		panel.add(lblNewLabel);
		
		textField = new JTextField();
		textField.setColumns(25);
		panel.add(textField);
		
		String [] models = {"J48", "MultilayerPerceptron"};
		JComboBox<String> comboBox = new JComboBox<String>(models);
		System.out.println(comboBox.getSelectedItem());
		contentPane.add(comboBox, BorderLayout.NORTH);
		
		JButton btnNewButton = new JButton("Choose Classifier");
		contentPane.add(btnNewButton, BorderLayout.SOUTH);
		btnNewButton.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent arg0) {
				
				String classifier = (String) comboBox.getSelectedItem();
			    Vector<String> classifierOptions = new Vector<String>();
			    String options = textField.getText();
			    StringTokenizer st = new StringTokenizer(options);
			    while (st.hasMoreTokens())
				    classifierOptions.add(st.nextToken());
			    			    
				try {
					control.setModel(classifier, classifierOptions, "ML_file/" + "TrainingSet.arff");
				} catch (Exception e) {
					e.printStackTrace();
				}
				
				dispose();
			}
		});
		
		setVisible(true);
		
	}

}
