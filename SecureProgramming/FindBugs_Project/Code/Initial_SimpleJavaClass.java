package sindu.simplejavaproject;
import java.io.*;
import java.util.*;
/**** SimpleJavaClass prints the folder structure of a directory ****/
public class SimpleJavaClass {
	public static void main(String[] args) {
		File driveOrDirName = new File("C:\\Users\\Default\\Documents");
	      FileFilter fileFil = new FileFilter() {
	         public boolean accept(File file) {
	            return file.isDirectory();
	         }
	      };
	      File[] folderOrFileList = driveOrDirName.listFiles(fileFil);
	      
	      if (folderOrFileList.length == 0) {
	         System.out.println("The given directory does not exist. Please verify and provide a valid path.");
	      } else {
	    	 System.out.println("Directory contains: " + folderOrFileList.length + " folders");
	         for (int i = 0; i< folderOrFileList.length; i++) {
	            File pathName = folderOrFileList[i];
	            System.out.println(pathName.toString());
	         }
	      }
	}
}
