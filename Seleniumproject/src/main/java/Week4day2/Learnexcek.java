package Week4day2;

public class Learnexcek {

	public static  void main(String[] args) {
		// TODO Auto-generated method stub
		//Step 1 : Setup the path for the workbook
		XSSFWorkbook wb = new XSSFWorkbook("./data/CreateLead.xlsx");
		//2 : Get in the respctive sheet 
		XSSFSheet ws = wb.getSheet("Sheet1");
		
		//Step 3 : Get in to the respective row 
		XSSFCell cell = row.getRow(1);
		//Step 3 : Get in to the respective cell 
				XSSFCell cell = row.getCell(0);
	   //step5; Read the data from the cell
	  String data = cell.getStringCellValue();
	 System.out.print(data);
	 //6:Close the workbook
	 wb.close();
	 
	 using forloop
	 for(int i=1;i<=2;i++)
	 {
		 String data = ws.getRow(i).getCell(0).getStringCellValue();
		 System.out.prinln(data);
	 }
		
  
		

	}

}
