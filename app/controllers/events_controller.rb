class EventsController < ApplicationController
  skip_before_filter :verify_authenticity_token 

  def push
    # TODO do work here
    email = params[:email]
    time = params[:time]
    kind = params[:kind]

    user = User.find_by_email(email)

    if user.nil?
      render :json => {:status => "Error", :message => "Invalid user!"}
      return
    end

    real_event = nil
    if kind == "commit"
      real_event = Commit.new
      real_event.author_email = params[:author_email]
      real_event.message = params[:message]
      real_event.commit_hash = params[:commit_hash]
      real_event.active_branch = params[:active_branch]
      real_event.files = params[:files].to_i
      real_event.insertions = params[:insertions].to_i
      real_event.deletions = params[:deletions].to_i

    end

    if real_event.save
      event = Event.new
      event.kind = kind
      event.user_id = user.id
      event.data_id = real_event.id

      if event.save
        render :json => {:status => "OK"}
        return
      end
    end

    render :json => {:status => "Error", :message => "Failed to create event!"}
  end

  def pusherror
    render 'error'
  end

  def pull
    showall = params[:showall]
    user = User.find_by_email(params[:email])
    if !user
      render :json => {:status => "Error", :message => "No user found!"}
      return
    end

    total_events = []

    subs = Subscription.find_all_by_user_id(user.id)
    for sub in subs
      # get new events from the users we are subscribed to
      latest = sub.latest.to_i
      events = Event.where(["user_id = ? AND id > ?", sub.subscribee.id, showall ? 0 : latest])
      next if events.length == 0

      # TODO remove events that are too old (e.g. after 5 minutes)
      total_events += events

      # mark these grabbed events as old
      sub.latest = events[-1].id
      if !sub.save
        render :json => {:status => "Error", :message => "Failed to save subscription latest!"}
        return
      end
    end

    e = []
    ret = {:events => e}

    for event in total_events
      if event.kind == "commit"
        real_event = Commit.find(event.data_id)
      end
      h = {:kind => event.kind}
      h.merge!(real_event.attributes)
      e << h
    end

    render :json => ret
  end

  # GET /events
  # GET /events.xml
  def index
    @events = Event.all

    respond_to do |format|
      format.html # index.html.erb
      format.xml  { render :xml => @events }
    end
  end

  # GET /events/1
  # GET /events/1.xml
  def show
    @event = Event.find(params[:id])

    respond_to do |format|
      format.html # show.html.erb
      format.xml  { render :xml => @event }
    end
  end

  # GET /events/new
  # GET /events/new.xml
  def new
    @event = Event.new

    respond_to do |format|
      format.html # new.html.erb
      format.xml  { render :xml => @event }
    end
  end

  # GET /events/1/edit
  def edit
    @event = Event.find(params[:id])
  end

  # POST /events
  # POST /events.xml
  def create
    @event = Event.new(params[:event])

    respond_to do |format|
      if @event.save
        format.html { redirect_to(@event, :notice => 'Event was successfully created.') }
        format.xml  { render :xml => @event, :status => :created, :location => @event }
      else
        format.html { render :action => "new" }
        format.xml  { render :xml => @event.errors, :status => :unprocessable_entity }
      end
    end
  end

  # PUT /events/1
  # PUT /events/1.xml
  def update
    @event = Event.find(params[:id])

    respond_to do |format|
      if @event.update_attributes(params[:event])
        format.html { redirect_to(@event, :notice => 'Event was successfully updated.') }
        format.xml  { head :ok }
      else
        format.html { render :action => "edit" }
        format.xml  { render :xml => @event.errors, :status => :unprocessable_entity }
      end
    end
  end

  # DELETE /events/1
  # DELETE /events/1.xml
  def destroy
    @event = Event.find(params[:id])
    @event.destroy

    respond_to do |format|
      format.html { redirect_to(events_url) }
      format.xml  { head :ok }
    end
  end
end
