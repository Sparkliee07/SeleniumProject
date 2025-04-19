package JavaAdvanceOOPS;

public interface SmartWatch extends Watch {
	
	public Boolean connectToPhone();
	public boolean turnBluetooth();
	public int getStepCount();
	public int getHeartBeat();
	public void setGoal(int steps);

}
