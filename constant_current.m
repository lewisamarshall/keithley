function [V, I, t]=constant_current(I_i, file, V_max, file2load)
	% CONSTANT_CURRENT is a script for controlling a 
	% Keithley 2410 power supply to apply a constant current. 
	% Base script written by Moran Bercovici, Jan 2008
	% Function wrapper written by Lewis Marshall, 2013. 

	% Set default variables. 
	
	if ~exist('I_i', 'var')
		I_i=1e-6;					% Default to applying 1 µA. 
	end

	if ~exist('file', 'var')
		file='current_trace.txt';	% Set the default file save location.
	end
	
	if ~exist('V_max', 'var')
		V_max=100;					% Set the default complience limit to 100 V. 
	end

	if ~exist('file2load', 'var')
		file2load={};				% If no files are specified, don't load anything.
	end

	% Select communication protocol. 

	ComProtocol='COM';      % GPIB/COM  - Communication protocol
	dt=0.0;                 % Additional delay time between measurements 

	WriteToFileFlag=1;      % 1/0 (Yes/No) Write results to file

	% Definitions for GPIB 
	%(Make sure the Keithley is set to the same PAD)
	GPIBID=1;               % GPIB iterface ID  (board index)
	PAD=20;                 % Instrument address (Primary address)

	% Definitions for COM
	%(Make sure the Keithley is set to the same values)
	%(Values listes here are the default on the Keithley)
	COMData={9600,8,'none',1,'CR'};

	% Plot the loaded files. 
	
	if ~isempty(File2Load)
	    for ij=1:length(File2Load)
	    A=load(File2Load{ij});
	    figure(1);
	    subplot(2,1,2);
	    plot(A(:,1),A(:,2),'b','linewidth',1); hold on;
	    end % for
	end

	% Select the com protocol. 
	switch (ComProtocol)
	    case('COM')
	        out=instrfind('Port','COM1');
	        if ~isempty (out)          
	        fclose(out);
	        end
	        g=serial('COM1');    
	      set(g,{'BaudRate','DataBits','Parity','StopBits','Terminator'},COMData)
	    case('GPIB')
	      g=gpib('ni',GPIBID,PAD);  % Define GPIB Device
	end

	% Open communications. 
	fopen(g);
	fprintf(g,'*RST');  %Restore GPIB defaults

	% ROUTING
	fprintf(g,':ROUT:TERM FRON');  %Use front panel jacks

	% SENSE COMMANDS
	fprintf(g,':SENS:FUNC:CONC 1');  %Set Concurrent measurements
	fprintf(g,':SENS:FUNC:ON "CURR", "VOLT"');  %Set voltage and current measurements
	%fprintf(g,':SENS:CURR:RANG 1e-6');   % Set expected reading in amps (for V-sourcing)
	fprintf(g,':SENS:CURR:RANG:AUTO 1'); % Set automatic range
	fprintf(g,[':SENS:VOLT:PROT ',num2str(VoltLim)]);   % Set current compliance limit (for V-sourcing)
	fprintf(g,':SENS:CURR:NPLC 1');      % Set integration time for measurements, based on power line cycles. i.e 1 --> 1/60 sec = 16.67 msec 
	fprintf(g,':SENS:AVER:STAT 0');      % Disable digital averaging filter (can be performed offline)

	% SOURCE COMMANDS
	fprintf(g,':SOUR:CLE:AUTO OFF');       % Disable auto output-off.  Output source will remain on after measurement, when system returns to idle
	fprintf(g,':SOUR:FUNC:MODE CURR');   % Set current sourcing
	fprintf(g,':SOUR:CURR:MODE FIX');    % Set fixed voltage value mode
	%fprintf(g,':SOUR:VOLT:RANG 500.0'); % Set voltage output range
	fprintf(g,':SOUR:CURR:RANG:AUTO 1'); % Enable automatic voltage range
	fprintf(g,[':SOUR:CURR ',num2str(Current)]); % Set output voltage  (immediate update, does not wait for trigger)

	% INITIATE SOURCING AND MEASUREMENTS
	%fprintf(g,':ARM:SOUR BUS')
	fprintf(g,':ARM:COUN 1');            % Set ARM counter to 1
	fprintf(g,':TRIG:COUN 1');           % Set trigger counter to 1 (will initiage 1 read after trigger)
	fprintf(g,':FORM:ELEM CURR, VOLT, TIME');  % Define output elements

	fprintf(g,':OUTP ON');                 % Turn on output

	% Open output file
	if WriteToFileFlag
	    fid=fopen(FileName,'w');
	    fprintf(fid,'%10s\t\t%10s\t\t%15s\n','%Time [s]','Voltage [V]','Current [A]');
	end

	ij=0;
	while 1
	    pause(dt);
	    ij=ij+1;
	    fprintf(g,':READ?')
	    OUT=str2num(fscanf(g));
	    CurrVec(ij)=OUT(2);
	    VoltVec(ij)=OUT(1);
	    TimeVec(ij)=OUT(3);
    
	    %figure(1);
	    subplot(2,1,1); plot(TimeVec-TimeVec(1),CurrVec,'r','linewidth',1);  xlabel ('Time [sec]'); ylabel ('Current [A]'); 
	    subplot(2,1,2); plot(TimeVec-TimeVec(1),VoltVec,'r');  xlabel ('Time [sec]'); ylabel ('Voltage [V]');  
	    drawnow;
    
	    if WriteToFileFlag
	        fprintf(fid,'%10.5f\t\t%5.5e\t\t%5.5e\n',[TimeVec(ij)'-TimeVec(1),VoltVec(ij)',CurrVec(ij)']');
	    end
    
	    keyIn = get(gcf, 'CurrentCharacter');
	    if strcmp(keyIn,'q') || strcmp(keyIn,'b')
	        break;
	    end;

	end

	if WriteToFileFlag
	    fclose(fid);
	end

	fprintf(g,':OUTP OFF');               % Turn off output
	fclose(g);

end



