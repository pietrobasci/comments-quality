package com.unisannio.controller;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Prova {

	public static void main(String[] args) throws IOException, InterruptedException {
		// TODO Auto-generated method stub

		String path = "/Users/pietrobasci/Documents/workspace/ProvaPython2/src/";
		String pkg = "web";
		
		String script1 = "script/ExtractCommentTotaliPerPackage.py";
		Process p = Runtime.getRuntime().exec("python" + " " + script1 + " " + path + " " + pkg);
		System.out.println("inizio");
		p.waitFor();
		System.out.println("fine");
		
		String script2 = "script/ContaComment.py";
	    Process p1 = Runtime.getRuntime().exec("python" + " " + script2 + " " + path + " " + pkg);
		p1.waitFor();
		
		String script3 = "script/POS.py";
		Process p2 = Runtime.getRuntime().exec("python" + " " + script3);
		p2.waitFor();
		
		String script4 = "script/Metrics2.py";
		Process p3 = Runtime.getRuntime().exec("python" + " " + script4 + " " + pkg);
		p3.waitFor();
		
		BufferedReader stdInput = new BufferedReader(new InputStreamReader(p3.getInputStream()));

		BufferedReader stdError = new BufferedReader(new InputStreamReader(p3.getErrorStream()));
		
           // read the output from the command
           System.out.println("Here is the standard output of the command:\n");
           String s=null;
           while ((s = stdInput.readLine()) != null) {
               System.out.println(s);
           }
           
           // read any errors from the attempted command
           System.out.println("Here is the standard error of the command (if any):\n");
           while ((s = stdError.readLine()) != null) {
               System.out.println(s);
           }
		
		
	}

}
