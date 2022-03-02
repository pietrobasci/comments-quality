package com.unisannio.gui;

import java.awt.BorderLayout;
import java.awt.EventQueue;
import java.awt.Font;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.IOException;

import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JSeparator;
import javax.swing.JTabbedPane;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import javax.swing.border.EmptyBorder;
import javax.swing.filechooser.FileNameExtensionFilter;

import com.unisannio.controller.AnalysisControl;




public class GUI extends JFrame {

	private static final long serialVersionUID = 1L;
	private JPanel contentPane;	
	private JTextField textField, textField1, textField2;
	private JButton btnBrowse, btnBrowse1, btnBrowse2;
	private AnalysisControl control;
    JFileChooser fc, fc1, fc2;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					GUI window = new GUI();
					window.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the application.
	 */
	public GUI() {
		initialize();
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		setBounds(100, 100, 820, 560);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		contentPane.setLayout(new BorderLayout(0, 0));
		setContentPane(contentPane);
		
		try {
			control = new AnalysisControl();
		} catch (Exception e1) {
			e1.printStackTrace();
		}
		
		
		JMenuBar menuBar = new JMenuBar();
		this.setJMenuBar(menuBar);
		
		JMenu mnFile = new JMenu("File");
		mnFile.setFont(new Font("Helvetica Neue", Font.PLAIN, 14));
		menuBar.add(mnFile);
		
		JMenuItem mntmMetrics = new JMenuItem("Metrics..");
		mntmMetrics.setFont(new Font("Helvetica Neue", Font.PLAIN, 14));
		mnFile.add(mntmMetrics);
		mntmMetrics.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent arg0) {
		        try {
					new GUIMetricsInfo(control.getMetrics());
				} catch (IOException e) {
					e.printStackTrace();
				}		
			}	
		});
		
		JMenuItem mntmModelInfo = new JMenuItem("Model info..");
		mntmModelInfo.setFont(new Font("Helvetica Neue", Font.PLAIN, 14));
		mnFile.add(mntmModelInfo);
		mntmModelInfo.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent arg0) {
		        new GUIModelInfo(control.getModelInfo());		
			}	
		});
		
		JMenu mnOption = new JMenu("Options");
		mnFile.setFont(new Font("Helvetica Neue", Font.PLAIN, 14));
		menuBar.add(mnOption);
		
		JMenuItem mntmChangeAlgorithm = new JMenuItem("Change Classifier");
		mntmChangeAlgorithm.setFont(new Font("Helvetica Neue", Font.PLAIN, 14));
		mnOption.add(mntmChangeAlgorithm);
		mntmChangeAlgorithm.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent arg0) {
				new GUISetAlgorithm(control);
			}
		});
		
		JLabel lblMultisala = new JLabel("/** Comments Quality */");
		lblMultisala.setBorder(new EmptyBorder(10, 0, 20, 0));
		lblMultisala.setFont(new Font("Helvetica Neue", Font.ITALIC, 55));
		lblMultisala.setHorizontalAlignment(SwingConstants.CENTER);
		contentPane.add(lblMultisala, BorderLayout.NORTH);
		
		JTabbedPane tabbedPane = new JTabbedPane(JTabbedPane.TOP);
		contentPane.add(tabbedPane, BorderLayout.CENTER);
		
		
		//tab class
		JPanel panel_3 = new JPanel();
		panel_3.setBorder(new EmptyBorder(30, 20, 0, 20));
		tabbedPane.addTab("Class", null, panel_3, null);
		panel_3.setLayout(new GridLayout(10, 0, 0, 0));
		
		JLabel lblNewLabel2 = new JLabel("Select the class to analyze");
		lblNewLabel2.setHorizontalAlignment(SwingConstants.CENTER);
		panel_3.add(lblNewLabel2);
		
		JPanel panel2_2 = new JPanel();
		panel_3.add(panel2_2);
		
		JLabel lblNewLabel2_3 = new JLabel("Path: ");
		lblNewLabel2_3.setHorizontalAlignment(SwingConstants.CENTER);
		panel2_2.add(lblNewLabel2_3);
		
		textField2 = new JTextField();
		panel2_2.add(textField2);
		textField2.setColumns(40);
		
        fc1 = new JFileChooser();
        fc1.setFileSelectionMode(JFileChooser.FILES_ONLY);
        //fc1.addChoosableFileFilter(new FileNameExtensionFilter("testo", "txt"));
        fc1.setFileFilter(new FileNameExtensionFilter("Class (.java)", "java"));
        fc1.setAcceptAllFileFilterUsed(false);

		JProgressBar progressBar2 = new JProgressBar();
        
		JLabel lblNewLabel2_2 = new JLabel();
		lblNewLabel2_2.setFont(new Font("Lucida Grande", Font.BOLD | Font.ITALIC, 30));
		lblNewLabel2_2.setHorizontalAlignment(SwingConstants.CENTER);
        
		btnBrowse1 = new JButton("Browse...");
        btnBrowse1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int returnVal = fc1.showOpenDialog(GUI.this);
				if (returnVal == JFileChooser.APPROVE_OPTION) {
	                File file = fc1.getSelectedFile();
	                textField2.setText(file.getPath());
					lblNewLabel2_2.setText("");
					progressBar2.setValue(0);
	            }/* else {
	            	textField1.setText("Open command cancelled by user.");
	            }*/
			    } 
			});
		panel2_2.add(btnBrowse1);
		
		JSeparator separator2 = new JSeparator();
		separator2.setVisible(false);
		panel_3.add(separator2);
		
		JSeparator separator2_1 = new JSeparator();
		separator2_1.setVisible(false);
		panel_3.add(separator2_1);
		
		JSeparator separator2_3 = new JSeparator();
		separator2_3.setVisible(false);
		panel_3.add(separator2_3);

		JButton btnAnalyze2 = new JButton("Analyze");
		btnAnalyze2.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				String path = textField2.getText();
				if (!path.isEmpty())
					try {
						double classQuality = control.analizeClass(path);
						switch ((int) classQuality){
					        case 0:
						        progressBar2.setValue(5);
						        lblNewLabel2_2.setText("Very Low");
						        break;
					        case 1:
						        progressBar2.setValue(25);
						        lblNewLabel2_2.setText("Low");
						        break;
					        case 2:
						        progressBar2.setValue(50);
						        lblNewLabel2_2.setText("Medium");
						        break;
					        case 3:
						        progressBar2.setValue(75);
						        lblNewLabel2_2.setText("High");
						        break;
					        case 4:
						        progressBar2.setValue(100);
						        lblNewLabel2_2.setText("Very High");
						        break;
						}
					} catch (Exception e1) {
						e1.printStackTrace();
					}
			    } 
			});
		panel_3.add(btnAnalyze2);
		
		JSeparator separator2_2 = new JSeparator();
		panel_3.add(separator2_2);
		
		JLabel lblNewLabel2_1 = new JLabel("Quality level: ");
		lblNewLabel2_1.setFont(new Font("Lucida Grande", Font.BOLD | Font.ITALIC, 20));
		lblNewLabel2_1.setHorizontalAlignment(SwingConstants.CENTER);
		panel_3.add(lblNewLabel2_1);
		
		panel_3.add(progressBar2);
		panel_3.add(lblNewLabel2_2);
		
		
		//tab package
		JPanel panel = new JPanel();
		panel.setBorder(new EmptyBorder(30, 20, 0, 20));
		tabbedPane.addTab("Package", null, panel, null);
		panel.setLayout(new GridLayout(10, 0, 0, 0));
		
		JLabel lblNewLabel = new JLabel("Select the package to analyze");
		lblNewLabel.setHorizontalAlignment(SwingConstants.CENTER);
		panel.add(lblNewLabel);
		
		JPanel panel_2 = new JPanel();
		panel.add(panel_2);
		
		JLabel lblNewLabel_3 = new JLabel("Path: ");
		lblNewLabel_3.setHorizontalAlignment(SwingConstants.CENTER);
		panel_2.add(lblNewLabel_3);
		
		textField = new JTextField();
		panel_2.add(textField);
		textField.setColumns(40);
		
        fc = new JFileChooser();
        fc.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);

		JProgressBar progressBar = new JProgressBar();
        
		JLabel lblNewLabel_2 = new JLabel();
		lblNewLabel_2.setFont(new Font("Lucida Grande", Font.BOLD | Font.ITALIC, 30));
		lblNewLabel_2.setHorizontalAlignment(SwingConstants.CENTER);
		
		btnBrowse = new JButton("Browse...");
        btnBrowse.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int returnVal = fc.showOpenDialog(GUI.this);
				if (returnVal == JFileChooser.APPROVE_OPTION) {
	                File file = fc.getSelectedFile();
	                textField.setText(file.getPath());
	                lblNewLabel_2.setText("");
	        		progressBar.setValue(0);
	            }/* else {
	            	textField.setText("Open command cancelled by user.");
	            }*/
			    } 
			});
		panel_2.add(btnBrowse);
		
		JSeparator separator = new JSeparator();
		separator.setVisible(false);
		panel.add(separator);
		
		JSeparator separator_1 = new JSeparator();
		separator_1.setVisible(false);
		panel.add(separator_1);
		
		JSeparator separator_3 = new JSeparator();
		separator_3.setVisible(false);
		panel.add(separator_3);
		
		JButton btnAnalyze = new JButton("Analyze");
		btnAnalyze.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				String path = textField.getText();
				if (!path.isEmpty())
					try {
						double packageQuality = control.analizePackage(path);
						switch ((int) packageQuality){
						    case 0:
							    progressBar.setValue(5);
							    lblNewLabel_2.setText("Very Low");
							    break;
						    case 1:
							    progressBar.setValue(25);
							    lblNewLabel_2.setText("Low");
							    break;
						    case 2:
							    progressBar.setValue(50);
							    lblNewLabel_2.setText("Medium");
							    break;
						    case 3:
							    progressBar.setValue(75);
							    lblNewLabel_2.setText("High");
							    break;
						    case 4:
							    progressBar.setValue(100);
							    lblNewLabel_2.setText("Very High");
							    break;
						}
					} catch (Exception e1) {
						e1.printStackTrace();
					}
			    } 
			});
		panel.add(btnAnalyze);
		
		JSeparator separator_2 = new JSeparator();
		panel.add(separator_2);
		
		JLabel lblNewLabel_1 = new JLabel("Quality level: ");
		lblNewLabel_1.setFont(new Font("Lucida Grande", Font.BOLD | Font.ITALIC, 20));
		lblNewLabel_1.setHorizontalAlignment(SwingConstants.CENTER);
		panel.add(lblNewLabel_1);
		
		panel.add(progressBar);
		panel.add(lblNewLabel_2);
		
		
		//tab project
		JPanel panel_1 = new JPanel();
		panel_1.setBorder(new EmptyBorder(30, 20, 0, 20));
		tabbedPane.addTab("Project", null, panel_1, null);
		panel_1.setLayout(new GridLayout(10, 0, 0, 0));
		
		JLabel lblNewLabel1 = new JLabel("Select the project to analyze");
		lblNewLabel1.setHorizontalAlignment(SwingConstants.CENTER);
		panel_1.add(lblNewLabel1);
		
		JPanel panel1_2 = new JPanel();
		panel_1.add(panel1_2);
		
		JLabel lblNewLabel1_3 = new JLabel("Path: ");
		lblNewLabel1_3.setHorizontalAlignment(SwingConstants.CENTER);
		panel1_2.add(lblNewLabel1_3);
		
		textField1 = new JTextField();
		panel1_2.add(textField1);
		textField1.setColumns(40);
		
        fc2 = new JFileChooser();
        fc2.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);

		JProgressBar progressBar1 = new JProgressBar();
        
		JLabel lblNewLabel1_2 = new JLabel();
		lblNewLabel1_2.setFont(new Font("Lucida Grande", Font.BOLD | Font.ITALIC, 30));
		lblNewLabel1_2.setHorizontalAlignment(SwingConstants.CENTER);
		
		btnBrowse2 = new JButton("Browse...");
        btnBrowse2.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int returnVal = fc2.showOpenDialog(GUI.this);
				if (returnVal == JFileChooser.APPROVE_OPTION) {
	                File file = fc2.getSelectedFile();
	                textField1.setText(file.getPath());
					lblNewLabel1_2.setText("");
					progressBar1.setValue(0);
	            }/* else {
	            	textField1.setText("Open command cancelled by user.");
	            }*/
			    } 
			});
		panel1_2.add(btnBrowse2);
		
		JSeparator separator1 = new JSeparator();
		separator1.setVisible(false);
		panel_1.add(separator1);
		
		JSeparator separator1_1 = new JSeparator();
		separator1_1.setVisible(false);
		panel_1.add(separator1_1);
		
		JSeparator separator1_3 = new JSeparator();
		separator1_3.setVisible(false);
		panel_1.add(separator1_3);
		
		JButton btnAnalyze1 = new JButton("Analyze");
		btnAnalyze1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				String path = textField1.getText();
				if (!path.isEmpty())
					try {
						double projectQuality = control.analizeProject(path);
						switch ((int) projectQuality){
							case 0:
								progressBar1.setValue(5);
								lblNewLabel1_2.setText("Very Low");
								break;
							case 1:
								progressBar1.setValue(25);
								lblNewLabel1_2.setText("Low");
								break;
							case 2:
								progressBar1.setValue(50);
								lblNewLabel1_2.setText("Medium");
								break;
							case 3:
								progressBar1.setValue(75);
								lblNewLabel1_2.setText("High");
								break;
							case 4:
								progressBar1.setValue(100);
								lblNewLabel1_2.setText("Very High");
								break;
						}
					} catch (Exception e1) {
						e1.printStackTrace();
					}
			    } 
			});
		panel_1.add(btnAnalyze1);
		
		JSeparator separator1_2 = new JSeparator();
		panel_1.add(separator1_2);
		
		JLabel lblNewLabel1_1 = new JLabel("Quality level: ");
		lblNewLabel1_1.setFont(new Font("Lucida Grande", Font.BOLD | Font.ITALIC, 20));
		lblNewLabel1_1.setHorizontalAlignment(SwingConstants.CENTER);
		panel_1.add(lblNewLabel1_1);

		panel_1.add(progressBar1);
		panel_1.add(lblNewLabel1_2);

		
	}

}
