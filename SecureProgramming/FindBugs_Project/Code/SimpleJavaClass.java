package sindu.simplejavaproject;
import java.io.*;
import java.util.*;
import java.util.logging.FileHandler;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;
/**** SimpleJavaClass prints the folder structure of a directory ****/
public class SimpleJavaClass {
	public static final String DIRPATH = "C://Users//Default//Documents";
	public static final Logger logger = Logger.getLogger("MyLogFile");
	public static void main(String[] args) {
		try {
		File driveOrDirName = new File(DIRPATH);
		FileHandler fhandler = new FileHandler("C://Users//sindu//Documents//workspace//MySimpleLogFile.log");
		logger.addHandler(fhandler);
		SimpleFormatter formatter = new SimpleFormatter();  
		fhandler.setFormatter(formatter); 
	    FileFilter fileFil = file -> file.isDirectory();
	    File[] folderOrFileList = driveOrDirName.listFiles(fileFil);
	    if(folderOrFileList != null) {
			if (folderOrFileList.length > 0) {
				logger.log(Level.ALL,"Directory contains: {0} folders", folderOrFileList.length);
				for (int i = 0; i< folderOrFileList.length; i++) {
					File pathName = folderOrFileList[i];
					logger.log(Level.INFO,"Folder Name: {0} ", pathName.toString());
				}
			} else {
				logger.log(Level.INFO,"The given directory does not exist. Please verify and provide a valid path.");
			}
		}
		}
		catch(Exception ex) {
			logger.log(Level.ALL,ex.getMessage());
		}
	}
}
